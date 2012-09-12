# coding=UTF-8
# Author: Dennis Lutter <lad1337@gmail.com>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

import random
import unittest

import test_lib as test

import sys, os.path, time

from lib.configobj import ConfigObj

import sickbeard
import sickbeard.search as search
from sickbeard.tv import TVEpisode, TVShow
import sickbeard.common as c
from sickbeard.common import Quality
import sickbeard.common as Status
from sickbeard import helpers

import functional_test

class EpisodeWantedTest(test.SickbeardTestDBCase):
    def test_wanted_episode_with_matching_language(self):
        show = TVShow(121361, "en", "en")
        show.loadFromTVDB()
        show.audio_langs = "de:1|en:0"
        episode = show.getEpisode(1, 1)
        episode.status = Status.WANTED
        episode.saveToDB()

        self.assertTrue(show.wantEpisode(1, 1, Quality.HDTV, False, '', ["en"]))
        

        episode.audio_langs = ["en"]
        episode.status = Quality.compositeStatus(Status.DOWNLOADED, Quality.FULLHDBLURAY)
        episode.saveToDB()
        # Fetch the preferred language even if the quality isn't as good as the existing one
        self.assertTrue(show.wantEpisode(1, 1, Quality.HDTV, False, '', ["de"]))


        episode.audio_langs = ["de"]
        episode.status = Quality.compositeStatus(Status.DOWNLOADED, Quality.FULLHDBLURAY)
        episode.saveToDB()
        # If we're satisfid don't fetch lower quality
        self.assertFalse(show.wantEpisode(1, 1, Quality.HDTV, False, '', ["de"]))


        episode.audio_langs = ["de"]
        episode.saveToDB()
        # We've got german so we're satisfied :)
        self.assertFalse(show.wantEpisode(1, 1, Quality.HDTV, False, '', ["en"]))

    def test_functional(self):
        functional_test.main()

        show = TVShow(121361, "en", "en")
        show.loadFromTVDB()
        show.audio_langs = "de:1|en:0"
        show.saveToDB()

        sickbeard.backlogSearchScheduler.action.searchBacklog([show])
        
        global __INITIALIZED__, currentSearchScheduler, backlogSearchScheduler, \
            showUpdateScheduler, versionCheckScheduler, showQueueScheduler, \
            properFinderScheduler, autoPostProcesserScheduler, searchQueueScheduler, \
            started
        
        while (backlogSearchScheduler.thread.am_running()):
            time.sleep(1)
            print "still running backlog"

        sickbeard.saveAndShutdown()

    def __init__(self, something):
        super(EpisodeWantedTest, self).__init__(something)


if __name__ == '__main__':
    print "=================="
    print "STARTING - Multi Langauge TESTS"
    print "=================="
    print "######################################################################"
    suite = unittest.TestLoader().loadTestsFromTestCase(EpisodeWantedTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
