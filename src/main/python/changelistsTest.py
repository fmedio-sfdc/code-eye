import unittest
import changelists

class TestChangelists(unittest.TestCase):

    def test_bad_gus_id_is_skipped(self):
        badGusId = """Change 13149790 by s.chaturvedi@gridmanager:vm:10.252.18.250 on 2017/03/09 23:59:14
    https://gus.my.salesforce.com/a07B00000030Et
Affected files ...
... //app/main/core/chatter/java/src/core/userprofile/actions/OutOfOfficeAction.java#1 add"""
        self.assertEqual(changelists.parseFiles(badGusId), [])

    def test_file_parsing(self):
        cl = """Change 13149790 by s.chaturvedi@gridmanager:vm:10.252.18.250 on 2017/03/09 23:59:14
    https://gus.my.salesforce.com/a07B00000030Eta
Affected files ...
... //app/f1.java#1 edit
... //app/f2.java#2 edit"""
        files = changelists.parseFiles(cl)
        self.assertEqual(len(files), 2)
        self.assertEqual([f['filename'] for f in files], ['//app/f1.java#1', '//app/f2.java#2'])

if __name__ == '__main__':
    unittest.main()

