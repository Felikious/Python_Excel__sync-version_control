# This is a project made to help synchronize two excel files
# The way it works at the moment is it checks the two files and a 
# hidden version control file. It notices the changes that happened,
# and changes the unchanged file. This is made as a start project 
# to make something like a foreign key, on update cascade,
# but across different excel files, and then maybe different type of files.

# author: Felikious 

import pandas as pd
import numpy as np
import hashlib as hl
import zipfile as zf
import sys
import os
import shutil
from datetime import datetime
from collections import defaultdict


class Excel_Version_Control:
    
    def __init__(self, file1_path, file2_path, key_columns):

        self.file1_path = file1_path
        self.file2_path = file2_path

        # Accept a list of columns or a single column
        if isinstance(key_columns, str):
            self.key_columns = [key_columns]
        else:
            self.key_columns = key_columns

        self.change_log = []
        self.conflict_log = []


    def _are_rows_equal(self, row1, row2):
        """Compare two rows based only on the key_column (e.g., 'name')"""
        if row1 is None or row2 is None:
            return row1 is None and row2 is None
        
        for column in self.key_columns:
            val1 = row1[column] if self.key_column in row1 else None
            val2 = row2[column] if self.key_column in row2 else None

             # Check if both are NaN
            if pd.isna(val1) and pd.isna(val2):
                continue
            if val1!= val2:
                return False
        return True

        
    def _get_row_by_id(self, df, id_value):
        """Get row by ID or return None if not found"""
        matches = df[df['ID'] == id_value]
        return matches.iloc[0] if not matches.empty else None
        
    def _add_row(self, df, row):
        """Add a row to DataFrame"""
        return pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        
    def _remove_row_by_id(self, df, id_value):
        """Remove row by ID"""
        return df[df['ID'] != id_value]
        
    def _log_change(self, change_type, id_value, details):
        """Log a change with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.change_log.append({
            'timestamp': timestamp,
            'type': change_type,
            'id': id_value,
            'details': details
        })
        
    def _get_value_changes(self, old_row, new_row):
        """Get detailed value changes between two rows"""
        if old_row is None or new_row is None:
            return "Row added" if old_row is None else "Row removed"
            
        changes = []
        for col in old_row.index:
            old_val = old_row[col] if not pd.isna(old_row[col]) else "NaN"
            new_val = new_row[col] if not pd.isna(new_row[col]) else "NaN"
            
            if old_val != new_val:
                changes.append(f"  • {col}: {old_val} → {new_val}")
                
        return "\n".join(changes) if changes else "No value changes (row reference update)"
        
    def sync_files(self):
        """Main synchronization method with detailed change logging"""
        # Load data
        df1 = pd.read_excel(self.file1_path, engine='openpyxl')
        df2 = pd.read_excel(self.file2_path, engine='openpyxl')
        df_vc = pd.read_excel(self.vc_path, engine='openpyxl')
        
        # Ensure ID column exists
        if 'ID' not in df1.columns or 'ID' not in df2.columns or 'ID' not in df_vc.columns:
            raise ValueError("All files must have an 'ID' column")
        
        # Get all unique IDs from all files
        all_ids = set(df1['ID']).union(df2['ID']).union(df_vc['ID'])
        
        # Create a new resolved version control dataframe
        resolved_df = pd.DataFrame(columns=df_vc.columns)
        
        # Track changes
        change_counts = defaultdict(int)
        
        # Process each ID
        for id_value in sorted(all_ids):
            # Get rows from each file
            row1 = self._get_row_by_id(df1, id_value)
            row2 = self._get_row_by_id(df2, id_value)
            row_vc = self._get_row_by_id(df_vc, id_value)
            
            # Case 1: Row exists in version control
            if row_vc is not None:
                # Check if both files match version control
                match1 = self._are_rows_equal(row1, row_vc)
                match2 = self._are_rows_equal(row2, row_vc)
                
                if match1 and match2:
                    # No changes - keep version control row
                    resolved_df = self._add_row(resolved_df, row_vc)
                    self._log_change("NO_CHANGE", id_value, "Row matches version control in both files")
                    
                elif match1 and not match2:
                    # File2 changed - take file2's version
                    resolved_df = self._add_row(resolved_df, row2)
                    change_counts['modified'] += 1
                    changes = self._get_value_changes(row_vc, row2)
                    self._log_change("MODIFY", id_value, 
                                    f"Updated from File2\nChanges:\n{changes}")
                    
                elif not match1 and match2:
                    # File1 changed - take file1's version
                    resolved_df = self._add_row(resolved_df, row1)
                    change_counts['modified'] += 1
                    changes = self._get_value_changes(row_vc, row1)
                    self._log_change("MODIFY", id_value, 
                                    f"Updated from File1\nChanges:\n{changes}")
                    
                else:
                    # Both files have changes
                    if self._are_rows_equal(row1, row2):
                        # Both changed the same way - take either
                        resolved_df = self._add_row(resolved_df, row1)
                        change_counts['modified'] += 1
                        changes = self._get_value_changes(row_vc, row1)
                        self._log_change("MODIFY", id_value, 
                                        f"Both files updated identically\nChanges:\n{changes}")
                    else:
                        # Handle conflicting changes
                        resolved_df = self._add_row(resolved_df, row1)
                        change_counts['conflicts'] += 1
                        change_counts['modified'] += 1
                        
                        # Get detailed differences
                        changes1 = self._get_value_changes(row_vc, row1)
                        changes2 = self._get_value_changes(row_vc, row2)
                        
                        conflict_details = {
                            'id': id_value,
                            'vc_version': row_vc.to_dict(),
                            'file1_version': row1.to_dict() if row1 is not None else None,
                            'file2_version': row2.to_dict() if row2 is not None else None,
                            'resolution': 'file1'
                        }
                        self.conflict_log.append(conflict_details)
                        
                        self._log_change("CONFLICT", id_value, 
                                       f"Resolved using File1 version\n"
                                       f"File1 changes:\n{changes1}\n\n"
                                       f"File2 changes:\n{changes2}")
            
            # Case 2: New row (not in version control)
            else:
                # Row exists in both files
                if row1 is not None and row2 is not None:
                    if self._are_rows_equal(row1, row2):
                        # Both added the same row
                        resolved_df = self._add_row(resolved_df, row1)
                        change_counts['added'] += 1
                        self._log_change("ADD", id_value, "New row added from both files")
                    else:
                        # Conflict - take file1's version
                        resolved_df = self._add_row(resolved_df, row1)
                        change_counts['conflicts'] += 1
                        change_counts['added'] += 1
                        
                        conflict_details = {
                            'id': id_value,
                            'vc_version': None,
                            'file1_version': row1.to_dict(),
                            'file2_version': row2.to_dict(),
                            'resolution': 'file1'
                        }
                        self.conflict_log.append(conflict_details)
                        
                        diff = self._get_value_changes(row2, row1)
                        self._log_change("CONFLICT", id_value, 
                                       f"New row conflict - used File1 version\n"
                                       f"Differences between files:\n{diff}")
                # Row only in file1
                elif row1 is not None:
                    resolved_df = self._add_row(resolved_df, row1)
                    change_counts['added'] += 1
                    self._log_change("ADD", id_value, "New row added from File1")
                # Row only in file2
                elif row2 is not None:
                    resolved_df = self._add_row(resolved_df, row2)
                    change_counts['added'] += 1
                    self._log_change("ADD", id_value, "New row added from File2")
        
        # Save resolved files
        resolved_df.to_excel(self.vc_path, index=False, engine='openpyxl')
        resolved_df.to_excel(self.file1_path, index=False, engine='openpyxl')
        resolved_df.to_excel(self.file2_path, index=False, engine='openpyxl')
        
        # Log final save action
        self._log_change("SYSTEM", "ALL", 
                       f"Files synchronized. Total changes: "
                       f"{change_counts.get('added',0)} additions, "
                       f"{change_counts.get('modified',0)} modifications, "
                       f"{change_counts.get('conflicts',0)} conflicts")
        
        return change_counts, self.conflict_log
    
    def print_changes(self):
        """Print all changes made during synchronization"""
        print("\n" + "="*80)
        print("PETHEROS SYNCHRONIZATION REPORT")
        print("="*80)
        
        for i, change in enumerate(self.change_log, 1):
            print(f"\n#{i} [{change['timestamp']}] {change['type']} - ID: {change['id']}")
            print("-"*80)
            print(change['details'])
        
        print("\n" + "="*80)
        print("SYNCHRONIZATION COMPLETE")
        print("="*80)
    
    def generate_report(self):
        """Generate a detailed synchronization report"""
        report = []
        report.append("="*80)
        report.append("PETHEROS SYNCHRONIZATION REPORT")
        report.append("="*80)
        
        for i, change in enumerate(self.change_log, 1):
            report.append(f"\n#{i} [{change['timestamp']}] {change['type']} - ID: {change['id']}")
            report.append("-"*80)
            report.append(change['details'])
        
        report.append("\n" + "="*80)
        report.append("SYNCHRONIZATION COMPLETE")
        report.append("="*80)
        
        return "\n".join(report)

        

    


