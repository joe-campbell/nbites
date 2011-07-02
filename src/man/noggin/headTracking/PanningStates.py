import man.motion.HeadMoves as HeadMoves
from . import TrackingConstants as constants
from man.motion import MotionConstants

# ** # old method
def scanBall(tracker):
    """
    While ball is not in view, execute naive pans.
    If ball is in view, go to last diff state.
    """
    ball = tracker.brain.ball
    if tracker.target == ball and \
            tracker.target.vis.framesOn >= constants.TRACKER_FRAMES_ON_TRACK_THRESH:
        tracker.activeLocOn = False
        return tracker.goNow('ballTracking')
    #Here we choose where to look for the ball first
    if not tracker.brain.motion.isHeadActive():
        if ball.dist > HeadMoves.HIGH_SCAN_CLOSE_BOUND:
            tracker.helper.executeHeadMove(HeadMoves.HIGH_WIDE_SCAN_BALL)
        elif ball.dist > HeadMoves.MID_SCAN_CLOSE_BOUND and \
                ball.dist < HeadMoves.MID_SCAN_FAR_BOUND:
            tracker.helper.executeHeadMove(HeadMoves.MID_DOWN_WIDE_SCAN_BALL)
        else:
            tracker.helper.executeHeadMove(HeadMoves.FULL_SCAN_BALL)

    # # Instead because our ball information is poor, lets just do one
    # # scan and make sure we don't miss it.  If our ball EKF is better
    # # and trustworthy than we can put the above code back in
    # if not tracker.brain.motion.isHeadActive():
    #     tracker.helper.executeHeadMove(HeadMoves.FULL_SCAN_BALL)
    return tracker.stay()

# ** # old method
def spinScanBall(tracker):
    """
    If ball is in view, goes to state cycle decider.
    If ball is not in view, execute pans based on direction robot is spinning.
    """
    ball = tracker.brain.ball
    nav = tracker.brain.nav

    if tracker.target == ball and \
            tracker.target.vis.framesOn >= constants.TRACKER_FRAMES_ON_TRACK_THRESH:
        tracker.activeLocOn = False
        return tracker.goNow('ballSpinTracking')

    if nav.walkTheta > 0:
        tracker.headMove = HeadMoves.LEFT_EDGE_SCAN_BALL
    else:
        tracker.headMove = HeadMoves.RIGHT_EDGE_SCAN_BALL

    if not tracker.brain.motion.isHeadActive():
        tracker.helper.executeHeadMove(tracker.headMove)

    return tracker.stay()

# ** # old method
def scanning(tracker):
    """
    Repeatedly run the stored headScan.
    """
    if tracker.firstFrame():
        tracker.brain.motion.stopHeadMoves()
        tracker.helper.executeHeadMove(tracker.currentHeadScan)

    if not tracker.brain.motion.isHeadActive():
        tracker.activeLocOn = False
        tracker.helper.executeHeadMove(tracker.currentHeadScan)

    return tracker.stay()

# ** # old method
def locPans(tracker):
    """
    Repeatedly execute the headMove QUICK_PANS.
    """
    if tracker.firstFrame():
        tracker.brain.motion.stopHeadMoves()
        tracker.helper.executeHeadMove(HeadMoves.QUICK_PANS)

    if not tracker.brain.motion.isHeadActive():
        tracker.activeLocOn = False
        tracker.helper.executeHeadMove(HeadMoves.QUICK_PANS)

    return tracker.stay()

# ** # new method
def afterKickScan(tracker):
    """
    Looks in the direction the ball was kicked in.
    If the ball is seen, go to state 'ballTracking'.
    """
    if tracker.counter < 2:
        tracker.brain.motion.stopHeadMoves()
        tracker.helper.executeHeadMove(constants.KICK_DICT[tracker.kickName])

    if tracker.brain.ball.vis.framesOn > 2:
        return tracker.goLater('ballTracking')

    return tracker.stay()

# ** # old method
def panLeftOnce(tracker):
    """
    Pan to the left, then return to last diff state.
    """
    if tracker.firstFrame():
        tracker.brain.motion.stopHeadMoves()
        tracker.helper.panTo(HeadMoves.PAN_LEFT_HEADS)
        return tracker.stay()

    if not tracker.brain.motion.isHeadActive():
        return tracker.goLater(tracker.lastDiffState)
    return tracker.stay()

# ** # old method
def panRightOnce(tracker):
    """
    Pan to the right, then return to last diff state.
    """
    if tracker.firstFrame():
        tracker.brain.motion.stopHeadMoves()
        tracker.helper.panTo(HeadMoves.PAN_RIGHT_HEADS)
        return tracker.stay()

    if not tracker.brain.motion.isHeadActive():
        return tracker.goLater(tracker.lastDiffState)
    return tracker.stay()

# ** # old method
def panUpOnce(tracker):
    """
    Pan to up, then return to last diff state.
    """
    if tracker.firstFrame():
        tracker.brain.motion.stopHeadMoves()
        tracker.helper.panTo(HeadMoves.PAN_UP_HEADS)
        return tracker.stay()

    elif not tracker.brain.motion.isHeadActive():
        return tracker.goLater(tracker.lastDiffState)
    return tracker.stay()

# ** # old method
def postScan(tracker):
    """
    Repeatedly execute the headMove POST_SCAN.
    """
    if tracker.firstFrame() \
            or not tracker.brain.motion.isHeadActive():
        tracker.activeLocOn = False
        tracker.helper.executeHeadMove(HeadMoves.POST_SCAN)
    return tracker.stay()

# ** # old method
def activeLocScan(tracker):
    """
    Execute naive mid-height scans.
    If ball is visible, return to state 'activeTracking'.
    """
    if tracker.target.vis.on:
        return tracker.goLater('activeTracking')

    if tracker.firstFrame() \
            or not tracker.brain.motion.isHeadActive():
        tracker.helper.executeHeadMove(HeadMoves.MID_UP_SCAN_BALL)

    return tracker.stay()

# ** # old method
def returnHeadsPan(tracker):
    """
    Return the head angles to pre-active pan position.
    """
    if tracker.firstFrame():
        tracker.brain.motion.stopHeadMoves()
        tracker.helper.panTo(tracker.preActivePanHeads)
        return tracker.stay()

    if not tracker.brain.motion.isHeadActive() or \
            tracker.target.vis.on:
        tracker.helper.trackObject()
        return tracker.goLater(tracker.lastDiffState)
    return tracker.stay()

# ** # old method
def look(tracker):
    """
    Look continuously in stored direction.
    If ball is sighted, go to state 'ballTracking'
    """
    if tracker.firstFrame():
        tracker.brain.motion.stopHeadMoves()
        heads = HeadMoves.LOOK_HEADS[tracker.lookDirection]
        tracker.helper.panTo(heads)
        return tracker.stay()
    if tracker.brain.ball.vis.on:
        return tracker.goNow('ballTracking')
    return tracker.stay()

# ** # old method
def scanQuickUp(tracker):
    """
    Pan up quickly, back to original angles, then stop.
    """
    if tracker.firstFrame():
        tracker.isPreKickScanning = True

        # always true...
        if tracker.lastDiffState != 'panUpOnce' or \
                tracker.lastDiffState != 'returnHeadsPan':
            tracker.activePanUp = False
            tracker.scanningUp = False
            motionAngles = tracker.brain.sensors.motionAngles
            tracker.preActivePanHeads = (
                motionAngles[MotionConstants.HeadYaw],
                motionAngles[MotionConstants.HeadPitch])


    if tracker.activePanUp and \
            not tracker.scanningUp:
        tracker.activePanUp = False
        tracker.isPreKickScanning = False
        return tracker.goLater('stop')

    elif tracker.activePanUp and \
            tracker.scanningUp:
        tracker.scanningUp = False
        return tracker.goNow('returnHeadsPan')

    else:
        tracker.scanningUp = True
        tracker.activePanUp = True
        return tracker.goNow('panUpOnce')


MOTION_START_BUFFER = 2

# ** # old method
# anything that calls this should make sure that
# goalieActiveLoc is set to proper value ( most likely false)
def trianglePan(tracker):
    """
    Execute either a left or right scan. Then, return to original
    head angles.
    """
    motionAngles = tracker.brain.sensors.motionAngles
    tracker.preTriPanHeads = (
        motionAngles[MotionConstants.HeadYaw],
        motionAngles[MotionConstants.HeadPitch]
        )

    if tracker.brain.sensors.motionAngles[MotionConstants.HeadYaw] > 0:
        return tracker.goNow('trianglePanLeft')
    else :
        return tracker.goNow('trianglePanRight')

# ** # old method
def trianglePanLeft(tracker):
    if tracker.firstFrame():
        if tracker.goalieActiveLoc:
            tracker.helper.executeHeadMove(HeadMoves.GOALIE_POST_LEFT_SCAN)
        else:
            tracker.helper.executeHeadMove(HeadMoves.POST_LEFT_SCAN)

    elif not tracker.brain.motion.isHeadActive() and \
            tracker.counter > MOTION_START_BUFFER:
        return tracker.goLater('trianglePanReturn')

    return tracker.stay()

# ** # old method
def trianglePanRight(tracker):
    if tracker.firstFrame():
        if tracker.goalieActiveLoc:
            tracker.helper.executeHeadMove(HeadMoves.GOALIE_POST_RIGHT_SCAN)
        else:
            tracker.helper.executeHeadMove(HeadMoves.POST_RIGHT_SCAN)

    elif not tracker.brain.motion.isHeadActive() and \
            tracker.counter > MOTION_START_BUFFER:
        return tracker.goLater('trianglePanReturn')
    return tracker.stay()

# ** # old method
def trianglePanReturn(tracker):
    if tracker.firstFrame():
        # TODO! Should be look to ball.
        tracker.helper.panTo(tracker.preTriPanHeads)
    elif (not tracker.brain.motion.isHeadActive() and
          tracker.counter > MOTION_START_BUFFER)  or \
          tracker.target.vis.on:
        return tracker.goLater('ballTracking')
    return tracker.stay()

# ** # old method
def bounceUp(tracker):
    """
    Repeatedly pan head up, then down.
    """
    if tracker.firstFrame():
        tracker.helper.panTo(HeadMoves.PAN_UP_HEADS)
    elif not tracker.brain.motion.isHeadActive():
        return tracker.goLater('bounceDown')
    return tracker.stay()

# ** # old method
def bounceDown(tracker):
    """
    Repeatedly pan head down, then up.
    """
    if tracker.firstFrame():
        tracker.helper.panTo(HeadMoves.PAN_DOWN_HEADS)
    elif not tracker.brain.motion.isHeadActive():
        return tracker.goLater('bounceUp')
    return tracker.stay()

