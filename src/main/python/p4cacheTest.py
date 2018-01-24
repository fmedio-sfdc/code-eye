import unittest
import p4cache

class TestP4Path(unittest.TestCase):

    rev1 = """... #7 change 12898330 integrate on 2017/01/26 10:53:43 by autointeg@gridmanager:vm:10.252.14.128 (text) 'Autointegrate Change: [12897602'"""

    def test_parse_version(self):
        self.assertEqual(
                '7',
                p4cache.parse_revision(TestP4Path.rev1)['p4.version'],
                )

    def test_parse_change(self):
        self.assertEqual(
                '12898330',
                p4cache.parse_revision(TestP4Path.rev1)['p4.change'],
                )

    def test_parse_action(self):
        self.assertEqual(
                'integrate',
                p4cache.parse_revision(TestP4Path.rev1)['p4.action'],
                )

    def test_parse_date(self):
        self.assertEqual(
                '2017/01/26',
                p4cache.parse_revision(TestP4Path.rev1)['p4.date'],
                )

    def test_parse_time(self):
        self.assertEqual(
                '10:53:43',
                p4cache.parse_revision(TestP4Path.rev1)['p4.time'],
                )

    def test_parse_committer(self):
        self.assertEqual(
                'autointeg',
                p4cache.parse_revision(TestP4Path.rev1)['p4.committer'],
                )

    fileoutput1 = """//app/206/patch/core/search/java/src/search/solr/client/impl/SolrServerImpl.java
    ... #7 change 12898330 integrate on 2017/01/26 10:53:43 by autointeg@gridmanager:vm:10.252.14.128 (text) 'Autointegrate Change: [12897602'
    ... ... copy from //app/206/freeze/core/search/java/src/search/solr/client/impl/SolrServerImpl.java#7,#799
    ... #6 change 12743941 edit on 2016/12/21 09:34:19 by guillaume.kempf@gridmanager:vm:10.252.15.5 (text) 'Entity Prediction: use speciali'"""

    def test_extract_move_from(self):
        self.assertEqual('//app/206/freeze/core/search/java/src/search/solr/client/impl/SolrServerImpl.java#799', p4cache.extract_moved_from_path(TestP4Path.fileoutput1))

    def test_integrate_filelog(self):
        self.assertEqual(
                '//app/206/patch/core/search/java/src/search/solr/client/impl/SolrServerImpl.java#6',
                p4cache.parse_filelog(TestP4Path.fileoutput1)['filename'],
                )

    fileoutput2 = """//app/206/patch/core/search/java/src/search/solr/client/impl/SolrServerImpl.java
    ... #6 change 12743941 edit on 2016/12/21 09:34:19 by guillaume.kempf@gridmanager:vm:10.252.15.5 (text) 'Entity Prediction: use speciali'
    ... #5 change 12499418 edit on 2016/11/14 13:53:22 by ruy@ruy-wsm-blt (text) '206 CLCO: Integrating from //ap'"""

    def test_edit_filelog(self):
        self.assertEqual(
                '//app/206/patch/core/search/java/src/search/solr/client/impl/SolrServerImpl.java#5',
                p4cache.parse_filelog(TestP4Path.fileoutput2)['filename'],
                )

    # p4 filelog -s -t -m 2 "//app/208/patch/core/support/test/func/java/src/support/fieldservice/servicereport/template/ServiceReportTemplateEditorRTAUiTest.java#4"
    fileoutput3 = """//app/208/patch/core/support/test/func/java/src/support/fieldservice/servicereport/template/ServiceReportTemplateEditorRTAUiTest.java
... #4 change 13621003 edit on 2017/05/04 14:15:26 by tji@gridmanager:vm:10.252.15.251 (text) 'Test support.fieldservice.servi'
... #3 change 13589379 integrate on 2017/04/29 01:15:41 by autointeg@gridmanager:vm:10.252.12.224 (text) 'Autointegrate Change: [13589320'
... ... merge from //app/206/patch/core/support/test/func/java/src/support/fieldservice/servicereport/template/ServiceReportTemplateEditorRTAUiTest.java#5"""

    def test_merge_from_filelog(self):
        self.assertEqual(
                '//app/206/patch/core/support/test/func/java/src/support/fieldservice/servicereport/template/ServiceReportTemplateEditorRTAUiTest.java#5',
                p4cache.parse_filelog(TestP4Path.fileoutput3)['filename'],
                )

if __name__ == '__main__':
    unittest.main()

