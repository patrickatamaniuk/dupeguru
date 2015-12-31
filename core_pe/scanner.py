# Created By: Virgil Dupras
# Created On: 2009-10-18
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.gnu.org/licenses/gpl-3.0.html

from core.scanner import Scanner, ScanType

from . import matchblock, matchexif
from .cache import Cache

class ScannerPE(Scanner):
    cache_path = None
    match_scaled = False
    threshold = 75
    
    def _getmatches(self, files, j, scanbase=None):
        if self.scan_type == ScanType.FuzzyBlock:
            return matchblock.getmatches(files, self.cache_path, self.threshold, self.match_scaled, j, scanbase)
        elif self.scan_type == ScanType.ExifTimestamp:
            return matchexif.getmatches(files, self.match_scaled, j)
        else:
            raise Exception("Invalid scan type")
    
    def clear_picture_cache(self):
        cache = Cache(self.cache_path)
        cache.clear()
        cache.close()
    
