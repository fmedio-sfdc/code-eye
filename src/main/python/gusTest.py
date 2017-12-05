import unittest
import gus

from contextlib import contextmanager
from io import StringIO
import sys
import json

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestGus(unittest.TestCase):

    def test_happy_path(self):
        fileinfos = [ {'filename':'foo', 'p4.gusid':'id1'} ]
        gus.assignRecordTypes(fileinfos, {'id1':'type1'})
        self.assertEqual(fileinfos[0]['gus.worktype'], 'type1')

    def test_bad_gus_id(self):
        fileinfos = [ {'filename':'a'} ]
        with captured_output() as (std, err):
            gus.assignRecordTypes(fileinfos, {})
        self.assertIn('no gusid', err.getvalue().strip())

    def test_no_record_type(self):
        fileinfos = [ {'filename':'foo', 'p4.gusid':'id1'} ]
        with captured_output() as (std, err):
            gus.assignRecordTypes(fileinfos, {})
        self.assertIn('no gus record type', err.getvalue().strip())

    def test_integration(self):
        fileinfos = [ {'filename':'foo', 'p4.gusid':'id1'} ]
        with captured_output() as (std, err):
            gus.assignRecordTypes(fileinfos, {'id1':'Integrate'})
        self.assertIn('integration', err.getvalue().strip())

    def test_queryToGus(self):
        gusJson = json.loads("""{"done": true, "records": [
        {
             "Id": "a07B0000003V7G2IAK",
             "Type__c": "Bug",
             "attributes": {
                 "type": "ADM_Work__c",
                 "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003V7G2IAK"
             }
         }]}""")

        #self.assertEqual(gus.queryToIds(gusJson), 'integration')

    def test_foo(self):
        query = {
            "done": True,
            "records": [
                {
                    "Id": "a07B0000000IpWZIA0",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000000IpWZIA0"
                    }
                },
                {
                    "Id": "a07B0000002MMqlIAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002MMqlIAG"
                    }
                },
                {
                    "Id": "a07B0000002QwGEIA0",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002QwGEIA0"
                    }
                },
                {
                    "Id": "a07B0000002V1F6IAK",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002V1F6IAK"
                    }
                },
                {
                    "Id": "a07B0000002V1FMIA0",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002V1FMIA0"
                    }
                },
                {
                    "Id": "a07B0000002V1YFIA0",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002V1YFIA0"
                    }
                },
                {
                    "Id": "a07B0000002iSE5IAM",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002iSE5IAM"
                    }
                },
                {
                    "Id": "a07B0000002j8uwIAA",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002j8uwIAA"
                    }
                },
                {
                    "Id": "a07B0000002nSsqIAE",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002nSsqIAE"
                    }
                },
                {
                    "Id": "a07B0000002nhxAIAQ",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002nhxAIAQ"
                    }
                },
                {
                    "Id": "a07B0000002pHQJIA2",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002pHQJIA2"
                    }
                },
                {
                    "Id": "a07B0000002qNQYIA2",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002qNQYIA2"
                    }
                },
                {
                    "Id": "a07B0000002qaHcIAI",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002qaHcIAI"
                    }
                },
                {
                    "Id": "a07B0000002rI5WIAU",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002rI5WIAU"
                    }
                },
                {
                    "Id": "a07B0000002rIXuIAM",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002rIXuIAM"
                    }
                },
                {
                    "Id": "a07B0000002rYNDIA2",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002rYNDIA2"
                    }
                },
                {
                    "Id": "a07B0000002sYduIAE",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002sYduIAE"
                    }
                },
                {
                    "Id": "a07B0000002tPdbIAE",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002tPdbIAE"
                    }
                },
                {
                    "Id": "a07B0000002tXG3IAM",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002tXG3IAM"
                    }
                },
                {
                    "Id": "a07B0000002xZj3IAE",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002xZj3IAE"
                    }
                },
                {
                    "Id": "a07B00000030DmcIAE",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030DmcIAE"
                    }
                },
                {
                    "Id": "a07B00000030SnuIAE",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030SnuIAE"
                    }
                },
                {
                    "Id": "a07B00000030ffIIAQ",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030ffIIAQ"
                    }
                },
                {
                    "Id": "a07B00000030kwnIAA",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030kwnIAA"
                    }
                },
                {
                    "Id": "a07B00000030lp3IAA",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030lp3IAA"
                    }
                },
                {
                    "Id": "a07B00000030mXgIAI",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030mXgIAI"
                    }
                },
                {
                    "Id": "a07B00000030oK4IAI",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030oK4IAI"
                    }
                },
                {
                    "Id": "a07B00000030oVCIAY",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030oVCIAY"
                    }
                },
                {
                    "Id": "a07B00000030raLIAQ",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030raLIAQ"
                    }
                },
                {
                    "Id": "a07B00000030vceIAA",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030vceIAA"
                    }
                },
                {
                    "Id": "a07B00000030vlqIAA",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030vlqIAA"
                    }
                },
                {
                    "Id": "a07B00000030wHzIAI",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030wHzIAI"
                    }
                },
                {
                    "Id": "a07B00000030x4yIAA",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030x4yIAA"
                    }
                },
                {
                    "Id": "a07B00000030xZXIAY",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030xZXIAY"
                    }
                },
                {
                    "Id": "a07B00000030yEsIAI",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030yEsIAI"
                    }
                },
                {
                    "Id": "a07B00000030zgEIAQ",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030zgEIAQ"
                    }
                },
                {
                    "Id": "a07B00000031A75IAE",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000031A75IAE"
                    }
                },
                {
                    "Id": "a07B00000031KLnIAM",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000031KLnIAM"
                    }
                },
                {
                    "Id": "a07B000000323f2IAA",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B000000323f2IAA"
                    }
                },
                {
                    "Id": "a07B0000003266gIAA",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003266gIAA"
                    }
                },
                {
                    "Id": "a07B00000032CQ8IAM",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000032CQ8IAM"
                    }
                },
                {
                    "Id": "a07B00000032DIBIA2",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000032DIBIA2"
                    }
                },
                {
                    "Id": "a07B00000032FHAIA2",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000032FHAIA2"
                    }
                },
                {
                    "Id": "a07B00000036VULIA2",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000036VULIA2"
                    }
                },
                {
                    "Id": "a07B00000037MXsIAM",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000037MXsIAM"
                    }
                },
                {
                    "Id": "a07B00000038J6BIAU",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000038J6BIAU"
                    }
                },
                {
                    "Id": "a07B00000038isHIAQ",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000038isHIAQ"
                    }
                },
                {
                    "Id": "a07B00000039DFTIA2",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000039DFTIA2"
                    }
                },
                {
                    "Id": "a07B00000039Ec0IAE",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000039Ec0IAE"
                    }
                },
                {
                    "Id": "a07B0000003Ap2lIAC",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Ap2lIAC"
                    }
                },
                {
                    "Id": "a07B0000003CLCbIAO",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003CLCbIAO"
                    }
                },
                {
                    "Id": "a07B0000003DRXhIAO",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003DRXhIAO"
                    }
                },
                {
                    "Id": "a07B0000003F0SwIAK",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003F0SwIAK"
                    }
                },
                {
                    "Id": "a07B0000003F754IAC",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003F754IAC"
                    }
                },
                {
                    "Id": "a07B0000003F7aqIAC",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003F7aqIAC"
                    }
                },
                {
                    "Id": "a07B0000003FA7xIAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FA7xIAG"
                    }
                },
                {
                    "Id": "a07B0000003FAmqIAG",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FAmqIAG"
                    }
                },
                {
                    "Id": "a07B0000003FDooIAG",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FDooIAG"
                    }
                },
                {
                    "Id": "a07B0000003FG5wIAG",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FG5wIAG"
                    }
                },
                {
                    "Id": "a07B0000003FJ7oIAG",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FJ7oIAG"
                    }
                },
                {
                    "Id": "a07B0000003FNo0IAG",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FNo0IAG"
                    }
                },
                {
                    "Id": "a07B0000003FRNKIA4",
                    "Type__c": "Integrate",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FRNKIA4"
                    }
                },
                {
                    "Id": "a07B0000003FUEsIAO",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FUEsIAO"
                    }
                },
                {
                    "Id": "a07B0000003FZOaIAO",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FZOaIAO"
                    }
                },
                {
                    "Id": "a07B0000003FZuvIAG",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FZuvIAG"
                    }
                },
                {
                    "Id": "a07B0000003FaBXIA0",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FaBXIA0"
                    }
                },
                {
                    "Id": "a07B0000003FjCuIAK",
                    "Type__c": "Integrate",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FjCuIAK"
                    }
                },
                {
                    "Id": "a07B0000003Fk0CIAS",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Fk0CIAS"
                    }
                },
                {
                    "Id": "a07B0000003Fp9DIAS",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Fp9DIAS"
                    }
                },
                {
                    "Id": "a07B0000003G4w8IAC",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003G4w8IAC"
                    }
                },
                {
                    "Id": "a07B0000003GGiqIAG",
                    "Type__c": "Integrate",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003GGiqIAG"
                    }
                },
                {
                    "Id": "a07B0000003GR7FIAW",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003GR7FIAW"
                    }
                },
                {
                    "Id": "a07B0000003GRZOIA4",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003GRZOIA4"
                    }
                },
                {
                    "Id": "a07B0000003GoC8IAK",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003GoC8IAK"
                    }
                },
                {
                    "Id": "a07B0000003GtqRIAS",
                    "Type__c": "Integrate",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003GtqRIAS"
                    }
                },
                {
                    "Id": "a07B0000003H1R6IAK",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003H1R6IAK"
                    }
                },
                {
                    "Id": "a07B0000003H7HqIAK",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003H7HqIAK"
                    }
                },
                {
                    "Id": "a07B0000003H9DBIA0",
                    "Type__c": "Integrate",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003H9DBIA0"
                    }
                },
                {
                    "Id": "a07B0000003HO7rIAG",
                    "Type__c": "Integrate",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HO7rIAG"
                    }
                },
                {
                    "Id": "a07B0000003HQCdIAO",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HQCdIAO"
                    }
                },
                {
                    "Id": "a07B0000003HcfcIAC",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HcfcIAC"
                    }
                },
                {
                    "Id": "a07B0000003HndlIAC",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HndlIAC"
                    }
                },
                {
                    "Id": "a07B0000003Hx6SIAS",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Hx6SIAS"
                    }
                },
                {
                    "Id": "a07B0000003HxIgIAK",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HxIgIAK"
                    }
                },
                {
                    "Id": "a07B0000003I4TJIA0",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003I4TJIA0"
                    }
                },
                {
                    "Id": "a07B0000003IK3fIAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003IK3fIAG"
                    }
                },
                {
                    "Id": "a07B0000003IkKuIAK",
                    "Type__c": "Integrate",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003IkKuIAK"
                    }
                },
                {
                    "Id": "a07B0000003Iqq2IAC",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Iqq2IAC"
                    }
                },
                {
                    "Id": "a07B0000003LrmvIAC",
                    "Type__c": "Test Change",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003LrmvIAC"
                    }
                },
                {
                    "Id": "a07B0000003M4rQIAS",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003M4rQIAS"
                    }
                },
                {
                    "Id": "a07B0000003RfOqIAK",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003RfOqIAK"
                    }
                },
                {
                    "Id": "a07B0000003RilKIAS",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003RilKIAS"
                    }
                },
                {
                    "Id": "a07B0000003S27lIAC",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003S27lIAC"
                    }
                },
                {
                    "Id": "a07B0000003S7YCIA0",
                    "Type__c": "Test Change",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003S7YCIA0"
                    }
                },
                {
                    "Id": "a07B0000003SOAhIAO",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003SOAhIAO"
                    }
                },
                {
                    "Id": "a07B0000003SX92IAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003SX92IAG"
                    }
                },
                {
                    "Id": "a07B0000003Si7sIAC",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Si7sIAC"
                    }
                },
                {
                    "Id": "a07B0000003T2P5IAK",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003T2P5IAK"
                    }
                },
                {
                    "Id": "a07B0000003T4YeIAK",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003T4YeIAK"
                    }
                },
                {
                    "Id": "a07B0000003T8SgIAK",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003T8SgIAK"
                    }
                },
                {
                    "Id": "a07B0000003TCkeIAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003TCkeIAG"
                    }
                },
                {
                    "Id": "a07B0000003TE5LIAW",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003TE5LIAW"
                    }
                },
                {
                    "Id": "a07B0000003THjgIAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003THjgIAG"
                    }
                },
                {
                    "Id": "a07B0000003TiYGIA0",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003TiYGIA0"
                    }
                },
                {
                    "Id": "a07B0000003TiaqIAC",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003TiaqIAC"
                    }
                },
                {
                    "Id": "a07B0000003Tq6fIAC",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Tq6fIAC"
                    }
                },
                {
                    "Id": "a07B0000003VJbvIAG",
                    "Type__c": "Test Change",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003VJbvIAG"
                    }
                },
                {
                    "Id": "a07B0000003WYgGIAW",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003WYgGIAW"
                    }
                },
                {
                    "Id": "a07B0000003WYhsIAG",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003WYhsIAG"
                    }
                },
                {
                    "Id": "a07B0000003X04YIAS",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003X04YIAS"
                    }
                },
                {
                    "Id": "a07B0000003XDaGIAW",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003XDaGIAW"
                    }
                },
                {
                    "Id": "a07B0000003XDorIAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003XDorIAG"
                    }
                },
                {
                    "Id": "a07B0000003XMrHIAW",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003XMrHIAW"
                    }
                },
                {
                    "Id": "a07B0000003XU8VIAW",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003XU8VIAW"
                    }
                },
                {
                    "Id": "a07B0000003XjLgIAK",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003XjLgIAK"
                    }
                },
                {
                    "Id": "a07B0000003XkkaIAC",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003XkkaIAC"
                    }
                },
                {
                    "Id": "a07B0000003XmqiIAC",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003XmqiIAC"
                    }
                },
                {
                    "Id": "a07B0000003XqP7IAK",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003XqP7IAK"
                    }
                },
                {
                    "Id": "a07B0000003Xy24IAC",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Xy24IAC"
                    }
                },
                {
                    "Id": "a07B0000003Y03JIAS",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Y03JIAS"
                    }
                },
                {
                    "Id": "a07B0000003Y6RlIAK",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Y6RlIAK"
                    }
                },
                {
                    "Id": "a07B0000003YWmgIAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003YWmgIAG"
                    }
                },
                {
                    "Id": "a07B0000003YYARIA4",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003YYARIA4"
                    }
                },
                {
                    "Id": "a07B0000003ZuY0IAK",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003ZuY0IAK"
                    }
                },
                {
                    "Id": "a07B0000003Zy7CIAS",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Zy7CIAS"
                    }
                },
                {
                    "Id": "a07B0000003a2WTIAY",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003a2WTIAY"
                    }
                },
                {
                    "Id": "a07B0000003aJkRIAU",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003aJkRIAU"
                    }
                },
                {
                    "Id": "a07B0000003bnltIAA",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003bnltIAA"
                    }
                },
                {
                    "Id": "a07B0000003cAsjIAE",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003cAsjIAE"
                    }
                },
                {
                    "Id": "a07B0000003cXeLIAU",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003cXeLIAU"
                    }
                },
                {
                    "Id": "a07B0000003cZvQIAU",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003cZvQIAU"
                    }
                },
                {
                    "Id": "a07B0000003caEwIAI",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003caEwIAI"
                    }
                },
                {
                    "Id": "a07B0000003d7JgIAI",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003d7JgIAI"
                    }
                },
                {
                    "Id": "a07B0000003e1hrIAA",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003e1hrIAA"
                    }
                },
                {
                    "Id": "a07B0000003eZqDIAU",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003eZqDIAU"
                    }
                },
                {
                    "Id": "a07B0000003ftUdIAI",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003ftUdIAI"
                    }
                },
                {
                    "Id": "a07B0000003hqOrIAI",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003hqOrIAI"
                    }
                },
                {
                    "Id": "a07B0000003i6syIAA",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003i6syIAA"
                    }
                },
                {
                    "Id": "a07B0000003iXRVIA2",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003iXRVIA2"
                    }
                },
                {
                    "Id": "a07B0000003j0NfIAI",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003j0NfIAI"
                    }
                },
                {
                    "Id": "a07B0000003j7JRIAY",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003j7JRIAY"
                    }
                },
                {
                    "Id": "a07B0000003jeRxIAI",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003jeRxIAI"
                    }
                },
                {
                    "Id": "a07B0000003kHwuIAE",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003kHwuIAE"
                    }
                },
                {
                    "Id": "a07B0000003kUywIAE",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003kUywIAE"
                    }
                },
                {
                    "Id": "a07B0000003keCFIAY",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003keCFIAY"
                    }
                },
                {
                    "Id": "a07B0000003n71wIAA",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003n71wIAA"
                    }
                },
                {
                    "Id": "a07B0000003raKoIAI",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003raKoIAI"
                    }
                },
                {
                    "Id": "a07B0000003sMElIAM",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003sMElIAM"
                    }
                },
                {
                    "Id": "a07B0000003xqV3IAI",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003xqV3IAI"
                    }
                },
                {
                    "Id": "a07B0000003zelXIAQ",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003zelXIAQ"
                    }
                },
                {
                    "Id": "a07B00000043jR9IAI",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000043jR9IAI"
                    }
                },
                {
                    "Id": "a07B00000043Ol5IAE",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000043Ol5IAE"
                    }
                },
                {
                    "Id": "a07B0000002vTRNIA2",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000002vTRNIA2"
                    }
                },
                {
                    "Id": "a07B00000030ho6IAA",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030ho6IAA"
                    }
                },
                {
                    "Id": "a07B00000030sRAIAY",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030sRAIAY"
                    }
                },
                {
                    "Id": "a07B00000030u8nIAA",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030u8nIAA"
                    }
                },
                {
                    "Id": "a07B00000030wceIAA",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030wceIAA"
                    }
                },
                {
                    "Id": "a07B00000030ylZIAQ",
                    "Type__c": "Test Case",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000030ylZIAQ"
                    }
                },
                {
                    "Id": "a07B000000356wMIAQ",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B000000356wMIAQ"
                    }
                },
                {
                    "Id": "a07B00000035TkFIAU",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B00000035TkFIAU"
                    }
                },
                {
                    "Id": "a07B0000003CK90IAG",
                    "Type__c": "Non Deterministic Test",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003CK90IAG"
                    }
                },
                {
                    "Id": "a07B0000003D76pIAC",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003D76pIAC"
                    }
                },
                {
                    "Id": "a07B0000003DQy5IAG",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003DQy5IAG"
                    }
                },
                {
                    "Id": "a07B0000003EwfrIAC",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003EwfrIAC"
                    }
                },
                {
                    "Id": "a07B0000003FAvdIAG",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FAvdIAG"
                    }
                },
                {
                    "Id": "a07B0000003FzbxIAC",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003FzbxIAC"
                    }
                },
                {
                    "Id": "a07B0000003G3AoIAK",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003G3AoIAK"
                    }
                },
                {
                    "Id": "a07B0000003GXLnIAO",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003GXLnIAO"
                    }
                },
                {
                    "Id": "a07B0000003GZBmIAO",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003GZBmIAO"
                    }
                },
                {
                    "Id": "a07B0000003GnouIAC",
                    "Type__c": "Integrate",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003GnouIAC"
                    }
                },
                {
                    "Id": "a07B0000003Gt4oIAC",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Gt4oIAC"
                    }
                },
                {
                    "Id": "a07B0000003HCmzIAG",
                    "Type__c": "Test Tool",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HCmzIAG"
                    }
                },
                {
                    "Id": "a07B0000003HD1RIAW",
                    "Type__c": "Test Case",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HD1RIAW"
                    }
                },
                {
                    "Id": "a07B0000003HNypIAG",
                    "Type__c": "Test Change",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HNypIAG"
                    }
                },
                {
                    "Id": "a07B0000003HO6tIAG",
                    "Type__c": "Integrate",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HO6tIAG"
                    }
                },
                {
                    "Id": "a07B0000003HPZLIA4",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HPZLIA4"
                    }
                },
                {
                    "Id": "a07B0000003HR4nIAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HR4nIAG"
                    }
                },
                {
                    "Id": "a07B0000003HhcIIAS",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HhcIIAS"
                    }
                },
                {
                    "Id": "a07B0000003Hk49IAC",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Hk49IAC"
                    }
                },
                {
                    "Id": "a07B0000003HuVPIA0",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003HuVPIA0"
                    }
                },
                {
                    "Id": "a07B0000003OoURIA0",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003OoURIA0"
                    }
                },
                {
                    "Id": "a07B0000003QUukIAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003QUukIAG"
                    }
                },
                {
                    "Id": "a07B0000003SoGIIA0",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003SoGIIA0"
                    }
                },
                {
                    "Id": "a07B0000003TQXkIAO",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003TQXkIAO"
                    }
                },
                {
                    "Id": "a07B0000003TepJIAS",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003TepJIAS"
                    }
                },
                {
                    "Id": "a07B0000003TiavIAC",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003TiavIAC"
                    }
                },
                {
                    "Id": "a07B0000003UAv4IAG",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003UAv4IAG"
                    }
                },
                {
                    "Id": "a07B0000003WFX5IAO",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003WFX5IAO"
                    }
                },
                {
                    "Id": "a07B0000003WYfwIAG",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003WYfwIAG"
                    }
                },
                {
                    "Id": "a07B0000003WiGdIAK",
                    "Type__c": "User Story",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003WiGdIAK"
                    }
                },
                {
                    "Id": "a07B0000003Wv8bIAC",
                    "Type__c": "Test Change",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003Wv8bIAC"
                    }
                },
                {
                    "Id": "a07B0000003YBP4IAO",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003YBP4IAO"
                    }
                },
                {
                    "Id": "a07B0000003akvBIAQ",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003akvBIAQ"
                    }
                },
                {
                    "Id": "a07B0000003eZz9IAE",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003eZz9IAE"
                    }
                },
                {
                    "Id": "a07B0000003f8SxIAI",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003f8SxIAI"
                    }
                },
                {
                    "Id": "a07B0000003kGWYIA2",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003kGWYIA2"
                    }
                },
                {
                    "Id": "a07B0000003nTrcIAE",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003nTrcIAE"
                    }
                },
                {
                    "Id": "a07B0000003oXQXIA2",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003oXQXIA2"
                    }
                },
                {
                    "Id": "a07B0000003xm1DIAQ",
                    "Type__c": "Test Failure",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003xm1DIAQ"
                    }
                },
                {
                    "Id": "a07B0000003yI5IIAU",
                    "Type__c": "Bug",
                    "attributes": {
                        "type": "ADM_Work__c",
                        "url": "/services/data/v20.0/sobjects/ADM_Work__c/a07B0000003yI5IIAU"
                    }
                }
            ],
            "totalSize": 200
        }
        self.assertEqual(len(gus.queryToIds(query)), 200)



if __name__ == '__main__':
    unittest.main()

