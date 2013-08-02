#!/usr/bin/env python
# coding: utf-8
#
# pyGTerm
#
# Copyright 2013, Sirmo Games S.A.
#
"""
Bindings for the gterm library
"""
#----------------------------------------------------------
# Standard library imports
#----------------------------------------------------------
from cython.operator cimport dereference as deref
from libcpp cimport bool
from libcpp.vector cimport vector

#----------------------------------------------------------
# SFML imports
#----------------------------------------------------------
from libsfml.sfml    cimport Vector2u, Vector2f, Color as sfColor, Vector3f
from libsfml.sfml    cimport IntRect as sfIntRect, FloatRect as sfFloatRect
from libsfml.sfml    cimport Time as sfTime, String as sfString
from libsfml.sfml    cimport seconds as sfSeconds
from libsfml.sfml    cimport milliseconds as sfMilliseconds
from libsfml.sfml    cimport microseconds as sfMicroSeconds
from libsfml.sfml    cimport Clock as sfClock
from libsfml.sfml    cimport BlendAlpha, BlendAdd, BlendMultiply, BlendNone
from libsfml.sfml    cimport Sound as sfSound, Music as sfMusic
from libsfml.sfml    cimport Stopped, Paused, Playing

#----------------------------------------------------------
# GTerm imports
#----------------------------------------------------------
from libgterm.config        cimport VERSION_MAJOR
from libgterm.config        cimport VERSION_MINOR
from libgterm.config        cimport VERSION_BUILD
from libgterm.window        cimport RenderWindow as cRenderWindow
from libgterm.application   cimport *
from libgterm.game          cimport Game as cGame
from libgterm.game_item     cimport GameItem as cGameItem
from libgterm.game_item_2d  cimport GameItem2D as cGameItem2D
from libgterm.sprite        cimport Sprite as cSprite
from libgterm.rectangle     cimport Rectangle as cRectangle
from libgterm.text_zone     cimport TextZone as cTextZone
from libgterm.text          cimport Text as cText
from libgterm.shadowed_text cimport ShadowedText as cShadowedText
from libgterm.button        cimport Button as cButton
from libgterm.gfx_score     cimport GfxScore as cGfxScore
from libgterm.gfx_display   cimport GfxDisplay as cGfxDisplay
from libgterm.grid          cimport Grid as cGrid
from libgterm.time_loop     cimport TimeLoop as cTimeLoop
from libgterm.animations    cimport Animation as cAnimation
from libgterm.animations    cimport AnimationBlink as cAnimationBlink, animDefineBlink
from libgterm.animations    cimport AnimationTexture as cAnimationTexture, animDefineTextureAnim, animLoadTextureAnim
from libgterm.animations    cimport FadeIn, FadeOut, AnimationFade as cAnimationFade, animDefineFade
from libgterm.animations    cimport AnimationRotation as cAnimationRotation, animDefineRotation
from libgterm.animations    cimport AnimationTranslation as cAnimationTranslation, animDefineTranslation
from libgterm.animations    cimport AnimationScale as cAnimationScale, animDefineScale
from libgterm.time_loop     cimport Wrap, Clamp, Forward, Backward
from libgterm.zone_file     cimport ZoneFile as cZoneFile, __cy__getZoneFile
from libgterm.config_file   cimport ConfigFile as cConfigFile
from libgterm.anchor        cimport Anchor_TopLeft, Anchor_TopCenter, Anchor_TopRight, Anchor_Left, Anchor_Center, Anchor_Right, Anchor_BottomLeft, Anchor_BottomCenter, Anchor_BottomRight, Anchor_Custom
from libgterm.rpc_status    cimport RPC_STATUS_NO_ERROR, RPC_STATUS_UNKNOWN_FCT, RPC_STATUS_BAD_ARG, RPC_STATUS_BAD_NB_ARG, RPC_STATUS_PENDING, RPC_STATUS_BAD_VERSION, RPC_STATUS_INTERNAL_ERR, RPC_STATUS_UNKNOWN_ERR, RPC_STATUS_ABORTED, RPC_STATUS_DELAYED, rpcStatusToString
from libgterm.rpc_frame     cimport RpcStack as cRpcStack, RpcFrame as cRpcFrame
from libgterm.rpc_command   cimport RpcParameter as cRpcParameter, RpcCommand as cRpcCommand, PA_BYTE, PA_WORD, PA_LONG, PA_RAW
from libgterm.rpc_handler   cimport CyRpcHandler
from libgterm.terminals     cimport TcpTerminalClient as cTcpTerminalClient
from libgterm.logger        cimport Error, Warning, Info
from libgterm.score         cimport Score as cScore

#----------------------------------------------------------
# Constants
#----------------------------------------------------------
#: The gterm c++ library version
import sys

GTERM_VERSION = "{0}.{1}.{2}".format(
    VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)
#: Represents an infinite value
INFINITE = 0xFFFFFFFF

#----------------------------------------------------------
# Signal slot
#----------------------------------------------------------
cdef class Signal(object):
    """
    Simple event system (inspired by c# delegates system).

    Taken from:

    http://www.voidspace.org.uk/python/weblog/arch_d7_2007_02_03.shtml#e616

    Don't forget to release any connection when disposeing an handler
    (using the -= operator to avoid circular references!
    """

    cdef list __slots

    def

    def __init__(self):
        self.__slots = []

    def clear(self):
        """
        Removes all slots
        """
        self.__slots[:] = []

    def __del__(self):
        self.clear()

    def connect(self, handler):
        """
        Connects a slot/handler to the signal
        """
        self.__slots.append( handler )
        self
        return self

    def disconnect(self, handler):
        """
        Disconnects the slot from the signal
        """
        self.__slots.remove( handler )
        return self

    def __call__(self, *args, **kwargs):
        """
        Emits the signal
        """
        ret_val = []
        for slot in self.__slots:
            val = slot( *args, **kwargs)
            if val is not None:
                ret_val.append(val)
        return ret_val

class GTermError(Exception):
    """
    GTerm exception
    """
    pass

#----------------------------------------------------------
# Generic callback function
#----------------------------------------------------------
cdef void __callback(void* f):
    """
    Generic callback methods used for every callback called from the c++ lib
    """
    (<object>f)()

#----------------------------------------------------------
# Enumerations
#----------------------------------------------------------
class Anchor(object):
    """
    Enumerates the possible anchors
    """
    TOP_LEFT        = Anchor_TopLeft
    TOP_CENTER      = Anchor_TopCenter
    TOP_RIGHT       = Anchor_TopRight
    LEFT            = Anchor_Left
    CENTER          = Anchor_Center
    RIGHT           = Anchor_Right
    BOTTOM_LEFT     = Anchor_BottomLeft
    BOTTOM_CENTER   = Anchor_BottomCenter
    BOTTOM_RIGHT    = Anchor_BottomRight
    CUSTOM          = Anchor_Custom
    CUSTOM

#----------------------------------------------------------
class BlendMode(object):
    """
    Enumerates the possible blend modes
    """
    #: Alpha blend mode
    ALPHA       = BlendAlpha
    #: Additive blend mode
    ADD         = BlendAdd
    #: Multiplicative blend mode
    MULTIPLY    = BlendMultiply
    #: No blending
    NONE        = BlendNone


#----------------------------------------------------------
class SoundStatus(object):
    """
    Enumerates the possible sound status
    """
    PAUSED = Paused
    STOPPED = Stopped
    PLAYING = Playing

#----------------------------------------------------------
class TextStyle(object):
    """
    Enumerates the possible text styles, those styles can be combined using
    the binary OR operator: |
    """
    #: Regular style (NONE)
    REGULAR     = 0
    #: Bold text
    BOLD        = 1
    #: Italic text
    ITALIC      = 2
    #: Underlined text
    UNDERLINED  = 4

#----------------------------------------------------------
class RpcStatus(object):
    """
    Enumerates teh
    """
    NO_ERROR = RPC_STATUS_NO_ERROR
    UNKNOWN_FCT = RPC_STATUS_UNKNOWN_FCT
    BAD_ARG = RPC_STATUS_BAD_ARG
    BAD_NB_ARGS = RPC_STATUS_BAD_NB_ARG
    PENDING = RPC_STATUS_PENDING
    BAD_VERSION = RPC_STATUS_BAD_VERSION
    INTERNAL_ERR = RPC_STATUS_INTERNAL_ERR
    UNKNOWN_ERR = RPC_STATUS_UNKNOWN_ERR
    ABORTED = RPC_STATUS_ABORTED
    DELAYED = RPC_STATUS_DELAYED


def rpc_status_to_string(status):
    """
    Returns the string representation of the rpc status
    """
    return rpcStatusToString(status)

#----------------------------------------------------------
class RpcParameterType(object):
    """
    Enumerates the possible rpc parameter types
    """
    BYTE = PA_BYTE   # 1 BYTE
    WORD = PA_WORD   # 2 BYTES
    LONG = PA_LONG   # 4 BYTES
    RAW  = PA_RAW    # Undetermined number of bytes (max = 251)


def param_type_to_string(ptype):
    """
    Convert a parameter type to a meaningful string

    :param ptype: The parameter type to convert to a string
    """
    if ptype == PA_BYTE:
        return "BYTE"
    elif ptype == PA_WORD:
        return "WORD"
    elif ptype == PA_LONG:
        return "LONG"
    elif ptype == PA_RAW:
        return "RAW"

#----------------------------------------------------------
# Memory management
#----------------------------------------------------------
cdef class _Disown(object):
    """
    Memory management flags. For most of the GTerm objects, the memory
    is managed internally. We use the _disown flag to prevent double free of the
    memory. (Whenever an object is added to another, _disown should be set to
    true)
    """
    cdef public bool _disown

    def __init__(self):
        self._disown = False

    property is_owned:
        def __get__(self):
            return self._disown


cdef class RenderWindow(object):
    cdef cRenderWindow m_window

    def set_resolution(self, resolution):
        self.m_window.setResolution(Vector2u(resolution[0], resolution[1]))

    def updateGame(self, Time elapsed_time, Game game):
        if game:
            self.m_window.updateGame(elapsed_time.m_time, game.thisptr)
        else:
            self.m_window.updateGame(elapsed_time.m_time, NULL)

    def drawGame(self, Game game):
        if game:
            self.m_window.drawGame(game.thisptr)
        else:
            self.m_window.drawGame(NULL)

    def create_from(self, handle):
        self.m_window.createFrom(handle)

    def display(self):
        self.m_window.display()

#----------------------------------------------------------
# Application
#----------------------------------------------------------
cdef class Application(object):
    """
    The Application class is the base class for creating GTerm
    applications.

    The application takes care of creating the main window
    and run the game loop. It manages a list of Games with only
    one active at the same time.

    There are different kinds of game screens in a gt application:
        - startup: this screens is rendered once when it is set so that
          the app can display something will loading the rest of the app
        - game: regular game screens or enterpanels
        - game selector: a game screen dedicated to draw the game selection
          screen
        - test game: a game screen dedicated to draw the test screens.
    """

    @classmethod
    def init_asset_manager(cls, data_path):
        initAssetManager(data_path, sys.argv[0])

    @classmethod
    def close_asset_manager(cls):
        closeAssetManager()

    @classmethod
    def create(self, name, version, version_key,
               resolution, dual_monitors=False, fullscreen=False,
               vsync=False, show_stats=False, data_path=""):
        """
        Creates the GTerm application

        :param name: version
        :type name: unicode

        :param version: version string
        :type version: unicode

        :param version_key: application version key
        :type version_key; int
        """
        create(name, version, version_key,
               Vector2u(resolution[0], resolution[1]), dual_monitors,
               fullscreen, vsync, show_stats, data_path, sys.argv[0])

    @classmethod
    def run(cls):
        """
        Runs the application main loop
        """
        run()

    @classmethod
    def add_game(self, Game game,  game_id):
        """
        Add a game/enterpanl to the application
        """
        game._disown = True
        addGame(game.thisptr, game_id)

    @classmethod
    def set_startup_game(self, Game game):
        """
        Sets the startup game. This should be called just after init and before
        any call to add_game
        """
        game._disown = True
        setStartupGame(game.thisptr)

    @classmethod
    def set_game_selector(self, Game game):
        """
        Sets the game selector
        """
        game._disown = True
        setGameSelector(game.thisptr)

    @classmethod
    def get_name(self):
        """
        Gets the application name
        """
        return getName()

    @classmethod
    def get_version(self):
        """
        Gets the application version
        """
        return getVersion()

    @classmethod
    def set_active_game(self, Game game):
        """
        Sets the active game
        """
        setActiveGame(game.thisptr)

    @classmethod
    def add_command(cls, RpcCommand cmd):
        """
        Adds an rpc command to the app
        """
        addCommand(cmd.m_cmd)

    @classmethod
    def get_command(cls, cmd_id):
        """
        Gets an rpc command by id
        """
        cdef RpcCommand cmd = RpcCommand("", 0, "", "")
        cmd.m_cmd = getCommand(cmd_id)
        return cmd

    @classmethod
    def get_commands(cls):
        """
        Gets the list of the application rpc commands
        """
        retVal = []
        commands = getRpcCommands()
        for c in commands:
            cmd = RpcCommand("", 0, "", 0)
            del cmd.m_cmd
            cmd.m_cmd = c
            retVal.append(cmd)
        return retVal

    @classmethod
    def postAnswer(cls, id, status):
        """
        Post an anwser for the specified command id. The answer if sent only
        if the specified command id is pending.
        """
        postAnswer(id, status)


    @classmethod
    def get_framerate(cls):
        return getFramerate()

#----------------------------------------------------------
# Games
#----------------------------------------------------------
cdef class Game(_Disown):
    """
    The Game class is the base class that represents a game
    screen. Final game object inherits from Game and add game items in the
    constructor (game items will be initalised at init time)

    A game is a list of game items. When updating a game, all game items are
    updated, when rendering a game all game items are rendered.

    Game items are stored in a map (name -> game item) for fast/easy access.
    They are also cached in an update list and render list, there the game items
    are sorted by their update/draw order.

    Client code can override update and draw methods to easily customize
    the way the game is update/rendered. Those two methods are empty by default.
    """
    cdef cGame* thisptr
    cdef object __init_func
    cdef object __draw_func
    cdef object __update_func
    cdef object __dict__

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cGame()

    def __dealloc__(self):
        if not self._disown:
            del self.thisptr

    def __init__(self, name):
        """
        Creates the game

        :param name: name of the game
        :type name: unicode
        """
        info("-- Loading %s" % name)
        _Disown.__init__(self)
        self.__dict__ = {}
        self.__init_func = None
        self.__draw_func = None
        self.__update_func = None
        self.thisptr.setName(name)
        self.__set_init_callback(self.on_init)
        self.__set_draw_callback(self.on_draw)
        self.__set_update_callback(self.on_update)

    def __getattr__(self, attr):
        try:
            return self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)

    def _setattr(self, name, value):
        self.__dict__[name] = value

    def __set_init_callback(self, func):
        self.thisptr.__cy__setInitCallback(__callback, <void*>func)
        self.__init_func = func

    def __set_update_callback(self, func):
        self.thisptr.__cy__setUpdateCallback(__callback, <void*>func)
        self.__update_func = func

    def __set_draw_callback(self, func):
        self.thisptr.__cy__setDrawCallback(__callback, <void*>func)
        self.__draw_func = func

    def add_game_item(self, GameItem2D item):
        """
        Adds a GameItem2D to the game scene

        :param item: GameItem2D to add
        """
        self.thisptr.addGameItem(item.thisptr)
        item._disown = True
        self._setattr(item.name, item)

    def get_game_item2d(self, name):
        """
        Gets a GameItem2D

        :param name: The name of the game item to get
        :type name: unicode

        :return: The researched game item 2d
        """
        gi = GameItem2D()
        del gi.thisptr
        gi.thisptr = <cGameItem2D*>self.thisptr.getGameItem(name)
        if gi.thisptr == NULL:
            return None
        gi._disown = True
        return gi

    def on_init(self):
        """
        Lets the user perform custom action when the game is initialised

        :param app: application instance
        :type app: pyGTerm.gterm.Application
        """
        pass

    def on_draw(self):
        """
        Lets the user perform custom action when the game is about to be drawn

        :param app: application instance
        :type app: pyGTerm.gterm.Application
        """
        pass

    def on_update(self):
        """
        Lets the user perform custom action when the game is about to be updated

        :param app: application instance
        :type app: pyGTerm.gterm.Application
        """
        pass

    def get_name(self):
        """
        Gets the game name

        :return the name of the game
        :rtype: unicode
        """
        return self.thisptr.getName()




#----------------------------------------------------------
# Game items
#----------------------------------------------------------
cdef class GameItem2D(_Disown):
    """
    The GameItem2D class is a concrete implementation of the GameItem interface
    focused on working in 2d with the SFML.

    The game item 2D is a game item contains, we can add child game item to
    it. Child game item's transform are attached to their parent to make up a
    scene graph (allow to group items together and make them follow the parent)


    .. note:: When you add an object (game item, sound, anim,...) to a game
              item, the object is set as a game item attribute (setattr). This
              allow the user to easily retrieve those objects. For example if
              you add an animation named "my_anim" to a game item gi. You can
              retrieve the animation instance by writing:: gi.my_anim
    """
    cdef public object __dict__
    cdef cGameItem2D* thisptr
    cdef object __init_func
    cdef object __draw_func
    cdef object __update_func
    cdef object __handlers

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cGameItem2D()

    def __init__(self, name, draw_order=0):
        """
        Creates the game item

        :param name; The name of the game item
        :type name: unicode

        :param draw_order: The draw order of the game item
        :type draw_order: int
        """
        self.__dict__ = {}
        self.thisptr.setName(name)
        self.thisptr.setDrawOrder(draw_order)
        self.__init_func = None
        self.__draw_func = None
        self.__update_func = None
        self.__handlers = []
        self.__set_init_callback(self.on_init)
        self.__set_draw_callback(self.on_draw)
        self.__set_update_callback(self.on_update)

    def _setattr(self, attr, value):
        self.__dict__[attr] = value

    def __getattr__(self, attr):
        try:
            return self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)

    def on_init(self):
        pass

    def on_update(self):
        pass

    def on_draw(self):
        pass

    def __set_init_callback(self, func):
        self.thisptr.__cy__setInitCallback(__callback, <void*>func)
        self.__init_func = func

    def __set_update_callback(self, func):
        self.thisptr.__cy__setUpdateCallback(__callback, <void*>func)
        self.__update_func = func

    def __set_draw_callback(self, func):
        self.thisptr.__cy__setDrawCallback(__callback, <void*>func)
        self.__draw_func = func

    property name:
        """
        The game item name/identifier
        """
        def __get__(self):
            return self.thisptr.getName()

    property position:
        """
        The game item position (tuple of float)
        """
        def __get__(self):
            return self.thisptr.getPosition().x, self.thisptr.getPosition().y

        def __set__(self, pos):
            self.thisptr.setPosition(pos[0], pos[1], 0.0)

    property rotation:
        """
        The game item rotation angle in degrees
        """
        def __set__(self, angle):
            self.thisptr.setRotation(0.0, 0.0, angle)

        def __get__(self):
            return self.thisptr.getRotation().z

    property scale:
        """
        The game item scale (tuple of float)
        """
        def __set__(self, scale):
            self.thisptr.setScale(scale[0], scale[1], 1)

        def __get__(self):
            return self.thisptr.getScale().x, self.thisptr.getScale().y

    def move(self, x, y):
        """
        Moves the game item

        :param x: distance to move on the X-Axis
        :type x: float

        :param y: distance to move on the Y-Axis
        :type y: float
        """
        self.thisptr.move(x, y, 0)

    def rotate(self, angle):
        """
        Rotates the game item

        :param angle: Amount of rotation
        :type angle: float
        """
        self.thisptr.rotate(0, 0, angle)

    def scale_(self, x, y):
        """
        Scales the game item

        :param x: Amount of scale on the X-Axis
        :type x: float

        :param y: Amount of scale on the Y-Axis
        :type y: float
        """
        self.thisptr.scale(x, y, 1)

    def set_initial_transform(self):
        """
        Sets the current transfom as the initial transform
        """
        self.thisptr.setInitialTransform()

    def reset_initial_transform(self):
        """
        Resets the initial transform
        """
        self.thisptr.resetInitalTransform()

    property draw_order:
        """
        The game item draw order
        """
        def __set__(self, do):
            self.thisptr.setDrawOrder(do)

        def __get__(self):
            return self.thisptr.getDrawOrder()

    def show(self):
        """
        Show the game item
        """
        self.thisptr.show()

    def hide(self):
        """
        Hides the game item
        """
        self.thisptr.hide()

    property visible:
        """
        The game item visibility.
        """
        def __set__(self, visible):
            if visible:
                self.show()
            else:
                self.hide()

        def __get__(self):
            """
            Checks if the game item is visible

            :return Whether the game item is visible or not
            :rtype bool
            """
            return self.thisptr.isVisible()

    def enable(self):
        """
        Enables the game item -> enable updates
        """
        self.thisptr.enable()

    def disable(self):
        """
        Disables the game item -> disable updates
        """
        self.thisptr.disable()

    property enabled:
        """
        The game item enable state
        """
        def __get__(self):
            return self.thisptr.isEnabled()

        def __set__(self, enable):
            if enable:
                self.enable()
            else:
                self.disable()

    def set_opacity(self, opacity, recursive=True):
        """
        Sets the game item opacity.

        :param opacity: Game item opacity [0.0 - 1.0]
        :type opacity: float

        :param recursive: Recursive flag. Set the opacity of all children if set
                          to true. Default is True
        :type recursive: bool
        """
        self.thisptr.setOpacity(opacity, recursive)

    def get_opacity(self):
        """
        Gets the game item opacity.

        :return The game item opacity
        :rtype float
        """
        return self.thisptr.getOpacity()

    def opacify(self, amount, recursive=True):
        """
        Modifies the game item opacity by the amount. The current opacity is
        multiplied by the amount

        :param amount: Amount of opacity to apply
        :type amount: float

        :param recursive: Apply the opacity recursively on all children
        :type recursive: bool
        """
        self.thisptr.opacify(amount, recursive)

    def set_use_scissor_mask(self, useScissor=False,
                             IntRect rect = IntRect(0, 0, 0, 0)):
        """
        Sets use scissor mask. This lets you specify an open gl scissor mask

        :param useScissor: True to use a scissor mask

        :param rect: The scissor mask as defined by opengl (origin os bottom
        left and the y axis goes upward)
        """
        self.thisptr.setUseScissorMask(useScissor, rect.m_rect)

    def add_game_item(self,GameItem2D game_item):
        """
        Adds a child game item

        :param game_item: The GameItem2D to add
        """
        self.thisptr.addGameItem(game_item.thisptr)
        game_item._disown = True
        self._setattr(game_item.name, game_item)

    def add_animation(self, Animation anim):
        """
        Adds an animation to the game item

        .. note:: the instance is set as an object attributes (the name is used
                  for the attribute id)
        """
        anim._disown = True
        self.thisptr.addAnimation(anim.thisptr)
        self._setattr(anim.name, anim)

    def add_sound(self, filename, name):
        """
        Adds a sound to the game item.

        .. note:: the instance is set as an object attributes (the name is used
                  for the attribute id)
        """
        cdef Sound snd = Sound()
        snd.thisptr = self.thisptr.addSound(filename, name)
        if snd.thisptr:
            self._setattr(name, snd)
            return snd
        return None

    def add_music(self, filename, name):
        """
        Adds a music to the game item.

        The music is set as a game item attribute (name if used for the attr
        name)
        """
        cdef Music msc = Music()
        msc.thisptr = self.thisptr.addMusic(filename, name)
        if msc.thisptr:
            self._setattr(name, msc)
            return msc
        return None

    def add_rpc_handler(self, RpcHandler handler):
        """
        Adds an rpc handler. The added handler is NOT RETRIEVABLE.
        """
        self.thisptr.addRpcHandler(handler.thisptr)
        self.__handlers.append(handler)


#----------------------------------------------------------
cdef class Sprite(GameItem2D):
    """
    The Sprite class is a GameItem2D specialised to draw a sprite based
    on sf::Sprite.
    """

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cSprite()

    def __init__(self, name, draw_order=0):
        """
        Creates the game item

        :param name; The name of the game item
        :type name: unicode

        :param draw_order: The draw order of the game item
        :type draw_order: int
        """
        GameItem2D.__init__(self, name, draw_order)
        self.thisptr.setName(name)
        self.thisptr.setDrawOrder(draw_order)

    property size:
        """
        Gets the size of the sprite as a tuple of floats
        """
        def __get__(self):
            cdef cSprite* sprite = <cSprite*> self.thisptr
            return sprite.getSize().x, sprite.getSize().y

    property anchor:
        """
        The sprite anchor type
        """
        def __set__(self, anchor):
            cdef cSprite* sprite = <cSprite*> self.thisptr
            sprite.setAnchor(anchor)

        def __get__(self):
            cdef cSprite* sprite = <cSprite*> self.thisptr
            return sprite.getAnchor()

    property anchor_point:
        """
        The sprite custom anchor point
        """
        def __set__(self, point):
            cdef cSprite* sprite = <cSprite*> self.thisptr
            sprite.setAnchorPoint(Vector2f(point[0], point[1]))

        def __get__(self):
            cdef cSprite* sprite = <cSprite*> self.thisptr
            return sprite.getAnchorPoint().x, \
                   sprite.getAnchorPoint().y

    property color:
        """
        The sprite modulation color.
        """
        def __set__(self, color):
            cdef cSprite* sprite = <cSprite*> self.thisptr
            sprite.setColor(sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cSprite* sprite = <cSprite*> self.thisptr
            sf_color = sprite.getColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property blend_mode:
        """
        The sprite blend mode (write only)
        """
        def __set__(self, value):
            cdef cSprite* sprite = <cSprite*> self.thisptr
            sprite.setBlendMode(value)

    def set_texture(self, filename):
        """
        Sets the sprite texture

        :param filename: Filename of the texture to set
        """
        cdef cSprite* sprite = <cSprite*> self.thisptr
        sprite.setTexture(filename)


    property name:
        """
        The sprite name, read only.
        """
        def __get__(self):
            return unicode(self.thisptr.getName())


#----------------------------------------------------------
cdef class Rectangle(GameItem2D):
    """
    The Rectangle class is a GameItem2D specialised to draw a rectangle based
    on sf::RectangleShape.
    """

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cRectangle()

    def __init__(self, name, draw_order=0, width=0, height=0):
        """
        Creates the game item

        :param name; The name of the game item
        :type name: unicode

        :param draw_order: The draw order of the game item
        :type draw_order: int
        """
        GameItem2D.__init__(self, name, draw_order)
        self.thisptr.setName(name)
        self.thisptr.setDrawOrder(draw_order)
        cdef cRectangle* rect = <cRectangle*> self.thisptr
        rect.setSize(Vector2f(width, height))

    property size:
        """
        Gets/Sets the rectangle size. The size is always a tuple of float (w, h)s
        """
        def __set__(self, size):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            rect.setSize(Vector2f(size[0], size[1]))

        def __get__(self):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            cdef Vector2f size = rect.getSize()
            return size.x, size.y

    property anchor:
        """
        Gets/Sets the rectangle anchor type
        """
        def __set__(self, anchor):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            rect.setAnchor(anchor)

        def __get__(self):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            return rect.getAnchor()

    property anchor_point:
        """
        Gets/Sets the rectangle custom anchor point
        """
        def __set__(self, point):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            rect.setAnchorPoint(Vector2f(point[0], point[1]))

        def __get__(self):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            return rect.getAnchorPoint().x, \
                   rect.getAnchorPoint().y

    property outline_color:
        """
        Gets/Sets the rectangle outline color.
        """
        def __set__(self, color):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            rect.setOutlineColor(sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            sf_color = rect.getOutlineColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property fill_color:
        """
        Gets/Sets the rectangle fill color.
        """
        def __set__(self, color):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            rect.setFillColor(sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            sf_color = rect.getFillColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property blend_mode:
        """
        Sets the rectangle blend mode (write only)
        """
        def __set__(self, value):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            rect.setBlendMode(value)

    property outline_thickness:
        """
        Gets/Sets the rectangle outline thickness
        """
        def __get__(self):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            return rect.getOutlineThickness()

        def __set__(self, value):
            cdef cRectangle* rect = <cRectangle*> self.thisptr
            rect.setOutlineThickness(value)


    def set_texture(self, filename):
        """
        Sets the sprite texture

        :param filename: Filename of the texture to set
        """
        cdef cSprite* sprite = <cSprite*> self.thisptr
        sprite.setTexture(filename)


    property name:
        """
        Gets the rectangle name
        """
        def __get__(self):
            return unicode(self.thisptr.getName())


#----------------------------------------------------------
cdef class TextZone(GameItem2D):
    """
    The TextZone class is a GameItem2D specialised to draw a TextZone based
    on sf::TextZoneShape.
    """

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cTextZone()

    def __init__(self, name, draw_order=0, width=0, height=0):
        """
        Creates the game item

        :param name; The name of the game item
        :type name: unicode

        :param draw_order: The draw order of the game item
        :type draw_order: int
        """
        GameItem2D.__init__(self, name, draw_order)
        self.thisptr.setName(name)
        self.thisptr.setDrawOrder(draw_order)
        cdef cTextZone* tz = <cTextZone*> self.thisptr
        tz.setSize(Vector2f(width, height))

    def set_score_value(self, value, nb_digits, nb_decimals):
        cdef cTextZone* text = <cTextZone*> self.thisptr
        text.setScoreValue(value, nb_digits, nb_decimals)

    def set_font(self, fn_font, ch_size):
        cdef cTextZone* tz = <cTextZone*> self.thisptr
        tz.setFont(fn_font, ch_size)

    property size:
        """
        Gets/Sets the TextZone size. The size is always a tuple of float (w, h)s
        """
        def __set__(self, size):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            tz.setSize(Vector2f(size[0], size[1]))

        def __get__(self):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            cdef Vector2f size = tz.getSize()
            return size.x, size.y

    property anchor:
        """
        Gets/Sets the TextZone anchor type
        """
        def __set__(self, anchor):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            tz.setAnchor(anchor)

        def __get__(self):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            return tz.getAnchor()

    property outline_color:
        """
        Gets/Sets the TextZone outline color.
        """
        def __set__(self, color):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            tz.setOutlineColor(sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            sf_color = tz.getOutlineColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property fill_color:
        """
        Gets/Sets the TextZone fill color.
        """
        def __set__(self, color):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            tz.setFillColor(sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            sf_color = tz.getFillColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property foreground_color:
        """
        Gets/Sets the TextZone fill color.
        """
        def __set__(self, color):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            tz.setForegroundColor(sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            sf_color = tz.getForegroundColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property blend_mode:
        """
        Sets the TextZone blend mode (write only)
        """
        def __set__(self, value):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            tz.setBlendMode(value)

    property outline_thickness:
        """
        Gets/Sets the TextZone outline thickness
        """
        def __get__(self):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            return tz.getOutlineThickness()

        def __set__(self, value):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            tz.setOutlineThickness(value)

    property string:
        """
        The text zone string (string that is displayed by the text item)
        """
        def __get__(self):
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            cdef char* decoded_string
            decoded_string = <char*>tz.getString().toAnsiString().c_str()
            return decoded_string.decode('utf-8')

        def __set__(self, string):
            cdef char* encoded_string
            cdef cTextZone* tz = <cTextZone*> self.thisptr
            encoded_string_temporary = string.encode('utf-8')
            encoded_string = encoded_string_temporary
            tz.setString(sfString(encoded_string))


    def set_texture(self, filename):
        """
        Sets the sprite texture

        :param filename: Filename of the texture to set
        """
        cdef cTextZone* tz = <cTextZone*> self.thisptr
        tz.setTexture(filename)


    property name:
        """
        Gets the TextZone name
        """
        def __get__(self):
            return unicode(self.thisptr.getName())


#----------------------------------------------------------
cdef class Text(GameItem2D):
    """
    The Text class is a GameItem2D specialised to draw text using
    sf::Text.
    """

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cText()

    def __init__(self, name, draw_order=0):
        """
        Creates the game item

        :param name; The name of the game item
        :type name: unicode

        :param draw_order: The draw order of the game item
        :type draw_order: int
        """
        GameItem2D.__init__(self, name, draw_order)
        self.thisptr.setName(name)
        self.thisptr.setDrawOrder(draw_order)

    property anchor:
        """
        The text anchor type
        """
        def __set__(self, anchor):
            cdef cText* text = <cText*> self.thisptr
            text.setAnchor(anchor)

        def __get__(self):
            """
            Gets the sprite anchor
            """
            cdef cText* text = <cText*> self.thisptr
            return text.getAnchor()

    property anchor_point:
        """
        The text custom anchor point
        """
        def __set__(self, point):
            cdef cText* text = <cText*> self.thisptr
            text.setAnchorPoint(point[0], point[1])

        def __get__(self):
            cdef cText* text = <cText*> self.thisptr
            return text.getAnchorPoint().x, \
                   text.getAnchorPoint().y

    property color:
        """
        The text color
        """
        def __set__(self, color):
            cdef cText* text = <cText*> self.thisptr
            text.setColor(sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cText* text = <cText*> self.thisptr
            sf_color = text.getColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property string:
        """
        The text string (string that is displayed by the text item)
        """
        def __get__(self):
            cdef cText* text = <cText*> self.thisptr
            cdef char* decoded_string
            decoded_string = <char*>text.getString().toAnsiString().c_str()
            return decoded_string.decode('latin-1')

        def __set__(self, string):
            cdef char* encoded_string
            cdef cText* text = <cText*> self.thisptr
            encoded_string_temporary = string.encode('latin-1')
            encoded_string = encoded_string_temporary
            text.setString(sfString(encoded_string))

    property font_name:
        """
        The text font filename. Default is "FONTS/Arial.ttf"
        """
        def __get__(self):
            cdef cText* text = <cText*> self.thisptr
            return text.getFontName()

        def __set__(self, font_name):
            cdef cText* text = <cText*> self.thisptr
            text.setFontName(font_name)

    property character_size:
        """
        The text character size in pixels
        """
        def __get__(self):
            cdef cText* text = <cText*> self.thisptr
            return text.getCharacterSize()

        def __set__(self, size):
            cdef cText* text = <cText*> self.thisptr
            text.setCharacterSize(size)

    property style:
        """
        The text style (Style.xxx).

        Styles can be combined as follow::
                text.style = gterm.TextStyle.BOLD | gterm.TextStyle.ITALIC
        """
        def __get__(self):
            cdef cText* text = <cText*> self.thisptr
            return text.getStyle()

        def __set__(self, style):
            cdef cText* text = <cText*> self.thisptr
            text.setStyle(style)

    def set_score_value(self, value, nb_digits, nb_decimals):
        cdef cText* text = <cText*> self.thisptr
        text.setScoreValue(value, nb_digits, nb_decimals)


#----------------------------------------------------------
cdef class ShadowedText(GameItem2D):
    """
    The ShadowedText class is a GameItem2D specialised to render a
    text with a shadow.

    The shadow effect is achieved by superposing two gt::Text with a slight
    offset. The background text is drawn with a dark slightly transparent color
    with a little offset in x and y.

    This class act as a wrapper over the main text game item and also provides
    methods to control the shadow color/opacity.
    """

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cShadowedText()

    def __init__(self, name, draw_order=0):
        """
        Creates the game item

        :param name; The name of the game item
        :type name: unicode

        :param draw_order: The draw order of the game item
        :type draw_order: int
        """
        GameItem2D.__init__(self, name, draw_order)
        self.thisptr.setName(name)
        self.thisptr.setDrawOrder(draw_order)

    def set_score_value(self, value, nb_digits, nb_decimals):
        cdef cShadowedText* text = <cShadowedText*> self.thisptr
        text.setScoreValue(value, nb_digits, nb_decimals)

    property anchor:
        """
        The shadowed text anchor type
        """
        def __set__(self, anchor):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            st.setAnchor(anchor)

        def __get__(self):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            return st.getAnchor()

    property anchor_point:
        """
        The custom anchor point
        """
        def __set__(self, point):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            st.setAnchorPoint(point[0], point[1])

        def __get__(self):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            return st.getAnchorPoint().x, \
                   st.getAnchorPoint().y

    property color:
        """
        The text color
        """
        def __set__(self, color):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            st.setColor(sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            sf_color = st.getColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property string:
        """
        The string to display
        """
        def __get__(self):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            cdef char* decoded_string
            decoded_string = <char*>st.getString().toAnsiString().c_str()
            return decoded_string.decode('utf-8')

        def __set__(self, string):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            cdef char* encoded_string
            encoded_string_temporary = string.encode('utf-8')
            encoded_string = encoded_string_temporary
            st.setString(sfString(encoded_string))

    property font_name:
        """
        The text font name. Default is "FONTS/Arial.ttf"
        """
        def __get__(self):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            return st.getFontName()

        def __set__(self, font_name):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            st.setFontName(font_name)

    property character_size:
        """
        The text character size in pixels
        """
        def __get__(self):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            return st.getCharacterSize()

        def __set__(self, size):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            st.setCharacterSize(size)

    property style:
        """
        The text style (Style.xxx).

        Styles can be combined as follow::
                text.style = gterm.TextStyle.BOLD | gterm.TextStyle.ITALIC
        """
        def __get__(self):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            return st.getStyle()

        def __set__(self, style):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            st.setStyle(style)

    property shadow_color:
        """
        The color of the text shadow
        """
        def __set__(self, color):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            st.setShadowColor(sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            sf_color = st.getShadowColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property shadow_offset:
        """
        The offset of the shadow relative to the text position.
        """
        def __set__(self, offset):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            st.setShadowOffset(Vector2f(offset[0], offset[1]))

        def __get__(self):
            cdef cShadowedText* st = <cShadowedText*> self.thisptr
            return st.getShadowOffset().x, st.getShadowOffset().y


#----------------------------------------------------------
cdef class Button(GameItem2D):
    """
     The Button class is a GameItem2D specialised to draw a button.
     A button is a sprite with two backgrounds:
        - one for the normal state
        - one for the pressed state
     The button is also able to display a text on top of the button image.

     There are convenience methods to retrieve the sub GameItems2D (the sprite
     and the text).

    The anchor of a button is always Center atm
    """
    def __cinit__(self, *args, **kargs):
        self.thisptr = new cButton()

    def __init__(self, name, draw_order=0):
        """
        Button ctor

        :param name: The game item name

        :param draw_order: The game item draw order
        """
        GameItem2D.__init__(self, name, draw_order)
        self.thisptr.setName(name)
        self.thisptr.setDrawOrder(draw_order)

    def set_textures(self, regular_texture, pressed_texture):
        """
        Sets the button textures

        :param regular_texture: Texture displayed when the button is not pressed

        :param pressed_texture: Texture displayed when the button is pressed
        """
        cdef cButton* bt = <cButton*> self.thisptr
        bt.setTextures(regular_texture, pressed_texture)

    def set_text_properties(self, string, font,
                            character_size, Color regular_color,
                            Color pressed_color):
        """
        Set the button text properties.

        If you don't call this method, the text is not displayed

        :param string: String to display
        :type string: unicode

        :param font; The text font name
        :type font: unicode

        :param character_size; The text character size
        :type character_size: int

        :param regular_color: Text text color used when the button is not
                              pressed
        :type regular_color: pyGTerm.gterm.Color

        :param pressed_color: Text text color used when the button is pressed
        :type pressed_color: pyGTerm.gterm.Color

        """
        cdef cButton* bt = <cButton*> self.thisptr
        cdef char* encoded_string
        encoded_string_temporary = string.encode('utf-8')
        encoded_string = encoded_string_temporary
        bt.setTextProperties(sfString(encoded_string),
                             font, character_size,
                             regular_color.m_color, pressed_color.m_color)

    property sprite:
        """
        The background sprite
        """
        def __get__(self):
            cdef cButton* bt = <cButton*> self.thisptr
            cdef cSprite* sprite = bt.getBackgroundSprite()
            s = Sprite(sprite.getName(), sprite.getDrawOrder())
            del s.thisptr
            s.thisptr = sprite
            s._disown = True
            return s

    property text:
        """
        The foreground text
        """
        def __get__(self):
            cdef cButton* bt = <cButton*> self.thisptr
            cdef cText* txt = bt.getText()
            s = Text(txt.getName(), txt.getDrawOrder())
            del s.thisptr
            s.thisptr = txt
            s._disown = True
            return s


#----------------------------------------------------------
cdef class GfxScore(GameItem2D):
    """
    The GfxScore class is a 2D game item specialised to render a score
    using a list of images instead of a regular font.

    The GFX font must be formatted as follow:
        - baseName_%d: Digits (0->9)
        - baseName_P: dot (.)
        - baseName_U: unit (?/$/£)
        - baseName_%c: Hexa (A->F)
    """

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cGfxScore()

    def __init__(self, name, draw_order=0, nb_digits=5, nb_decimal_digits=2):
        """
        Create the c++ instance

        :param name: game item name

        :param draw_order: game item draw order

        :param nb_digits: The total number of digits that can be displayed

        :param nb_decimal_digits: The number of decimal digits (should be less
                                  than nb_digits
        """
        GameItem2D.__init__(self, name, draw_order)
        cdef cGfxScore* gfx = <cGfxScore*> self.thisptr
        gfx.__init(nb_digits, nb_decimal_digits)
        self.thisptr.setName(name)
        self.thisptr.setDrawOrder(draw_order)

    property width:
        """
        The score local width
        """
        def __get__(self):
            cdef cGfxScore* gfx = <cGfxScore*> self.thisptr
            return gfx.getWidth()

    property score:
        """
        The score value
        """
        def __set__(self, value):
            cdef cGfxScore* gfx = <cGfxScore*> self.thisptr
            gfx.setScore(value)

        def __get__(self):
            cdef cGfxScore* gfx = <cGfxScore*> self.thisptr
            return gfx.getScore()

    property anchor:
        """
        The score anchor type
        """
        def __set__(self, anchor):
            cdef cGfxScore* gfx = <cGfxScore*> self.thisptr
            gfx.setAnchor(anchor)

        def __get__(self):
            cdef cGfxScore* gfx = <cGfxScore*> self.thisptr
            return gfx.getAnchor()

    property color:
        """
        The score modulation color. Write only
        """
        def __set__(self, color):
            cdef cGfxScore* gfx = <cGfxScore*> self.thisptr
            gfx.setColor(sfColor(color.r, color.g, color.b, color.a))

    def set_gfx_font(self, base_name, extension=".png"):
        """
        Sets the gfx font

        :param base_name: The font base name (without n° or extension)

        :param extension: The font extension. Default is ".png"
        """
        cdef cGfxScore* gfx = <cGfxScore*> self.thisptr
        gfx.setGfxFont(base_name, extension)


#----------------------------------------------------------
cdef class GfxDisplay(GameItem2D):
    """
    The GfxDisplay class is a 2D game item specialised to draw a display
    based on a GfxScore.

    A display is a background sprite + a GfxScore.
    """

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cGfxDisplay()

    def __init__(self, name, gfxFont, texture,
                 draw_order=0, nb_digits=5, nb_decimal_digits=2,
                 gfxFontExtension=".png"):
        """
        Create the c++ instance

        :param name: game item name

        :param gfxFont: Gfx font base name

        :param texture: Background texture

        :param gfxFontExtension: Gfx font extension. Default is png

        :param draw_order: game item draw order

        :param nb_digits: The total number of digits that can be displayed

        :param nb_decimal_digits: The number of decimal digits (should be less
                                  than nb_digits
        """
        GameItem2D.__init__(self, name, draw_order)
        self.thisptr.setName(name)
        self.thisptr.setDrawOrder(draw_order)
        cdef cGfxDisplay* gfx = <cGfxDisplay*> self.thisptr
        gfx.__init(nb_digits, nb_decimal_digits)
        gfx.setGfxFont(gfxFont, gfxFontExtension)
        gfx.setTexture(texture)

    property score:
        """
        The score value
        """
        def __set__(self, value):
            cdef cGfxDisplay* gfx = <cGfxDisplay*> self.thisptr
            gfx.setScore(value)

        def __get__(self):
            cdef cGfxDisplay* gfx = <cGfxDisplay*> self.thisptr
            return gfx.getScore()

    property anchor:
        """
        The display anchor type
        """
        def __set__(self, anchor):
            cdef cGfxDisplay* gfx = <cGfxDisplay*> self.thisptr
            gfx.setAnchor(anchor)

        def __get__(self):
            cdef cGfxDisplay* gfx = <cGfxDisplay*> self.thisptr
            return gfx.getAnchor()

    property score_color:
        """
        The score color
        """
        def __set__(self, color):
            cdef cGfxDisplay* gfx = <cGfxDisplay*> self.thisptr
            gfx.setScoreColor(sfColor(color.r, color.g, color.b, color.a))

    property background_sprite:
        """
        The background sprite
        """
        def __get__(self):
            cdef cGfxDisplay* gfx = <cGfxDisplay*> self.thisptr
            cdef cSprite* sp = gfx.getSprite()
            s = Sprite(sp.getName(), sp.getDrawOrder())
            del s.thisptr
            s.thisptr = sp
            s._disown = True
            return s

    property gfx_score:
        """
        The foreground score (GfxScore)
        """
        def __get__(self):
            cdef cGfxDisplay* gfx = <cGfxDisplay*> self.thisptr
            cdef cGfxScore* sc = gfx.getGfxScore()
            s = GfxScore(sc.getName(), sc.getDrawOrder())
            del s.thisptr
            s.thisptr = sc
            s._disown = True
            return s

    def set_gfx_font(self, base_name, extension=".png"):
        """
        Sets the gfx font

        :param base_name: The font base name (without n° or extension)

        :param extension: The font extension. Default is ".png"
        """
        cdef cGfxScore* gfx = <cGfxScore*> self.thisptr
        gfx.setGfxFont(base_name, extension)

    def set_texture(self, texture_filename):
        """
        Sets the background texture
        """
        cdef cGfxDisplay* gfx = <cGfxDisplay*> self.thisptr
        gfx.setTexture(texture_filename)


#----------------------------------------------------------
cdef class Grid(GameItem2D):
    """
    The Grid class is a GameItem2D specialised to draw a simple grid.

    The grid is a 2D array of gt::TextZone.

    Here are the most important properties:
        - nb_lines: number of lines
        - nb_columns: number of columns
        - line_height: all lines have the same height
        - column_widths: a list of width for each individual column
        - background_color: the cells background color
        - alternate_background_color and use_alternate_background color: defines
          if we alternate the row background color 1 line on 2.
        - font and font size: the grid text content font properties
        - font_color: the font color
        - selection_color: the selected line highlight color.
        - selected_line: index of the selected line, -1 to unselect
        - outline_color: color of the grid lines

    The grid setups default values for style properties. The default font is
    FONTS/arial.ttf

    .. note:: The grid dimensions must be set in the constructor and
              cannot be changed afterwards.
    """
    def __cinit__(self, *args, **kargs):
        self.thisptr = new cGrid()

    def __init__(self, name, nb_lines, nb_columns,
                 line_height, col_widths, draw_order=0):
        """
        :param name: Game item name
        :type name: unicode

        :param nb_lines: Number of lines in the grid
        :type nb_lines: int

        :param nb_columns: Number of columns in the grid
        :type nb_columns: int

        :param line_height: Line height in pixels
        :type line_height: float

        :param col_widths: List of column withs. The length MUST match
                           nb_columns
        :type col_widths: list of float
        """
        GameItem2D.__init__(self, name, draw_order)
        self.thisptr.setName(name)
        self.thisptr.setDrawOrder(draw_order)
        cdef cGrid* grd = <cGrid*> self.thisptr
        grd.__init(nb_lines, nb_columns, line_height, col_widths)

    property background_color:
        """
        The grid background color
        """
        def __set__(self, Color color):
            cdef cGrid* grd = <cGrid*> self.thisptr
            grd.setBackgroundColor(sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cGrid* grd = <cGrid*> self.thisptr
            sf_color = grd.getBackgroundColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property use_alternate_background_color:
        """
        Flag that specifies if we must use an alternate row color. If set to
        True, each even lines is filled with the background color and odd lines
        are filled with the alternate_background_color.
        """
        def __set__(self, bool value):
            cdef cGrid* grd = <cGrid*> self.thisptr
            grd.setUseAlternateBackgroundColor(value)

        def __get__(self):
            cdef cGrid* grd = <cGrid*> self.thisptr
            return grd.getUseAlternateBackgroundColor()

    property alternate_background_color:
        """
        The alternate background color, only used if
        use_alternate_background_color is True
        """
        def __set__(self, color):
            cdef cGrid* grd = <cGrid*> self.thisptr
            grd.setAlternateBackgroundColor(
                sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cGrid* grd = <cGrid*> self.thisptr
            sf_color = grd.getAlternateBackgroundColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property outline_color:
        """
        The outline color (color of the grid lines)
        """
        def __set__(self, color):
            cdef cGrid* grd = <cGrid*> self.thisptr
            grd.setOutlineColor(
                sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cGrid* grd = <cGrid*> self.thisptr
            sf_color = grd.getOutlineColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    property selection_color:
        """
        The selection color (used when calling select_line with a line index
        different from -1
        """
        def __set__(self, color):
            cdef cGrid* grd = <cGrid*> self.thisptr
            grd.setSelectionColor(
                sfColor(color.r, color.g, color.b, color.a))

        def __get__(self):
            cdef cGrid* grd = <cGrid*> self.thisptr
            sf_color = grd.getSelectionColor()
            return Color(sf_color.r, sf_color.g, sf_color.b, sf_color.a)

    def set_font(self, font_name, character_size, Color color):
        """
        Sets the grid font properties
        """
        cdef cGrid* grd = <cGrid*> self.thisptr
        grd.setFont(font_name, character_size,
                    sfColor(color.r, color.g, color.b, color.a))

    def select_line(self, index=-1):
        """
        Select a grid line.

        :param index: Index of the line to selectd. Use -1 to unselect lines
        """
        cdef cGrid* grd = <cGrid*> self.thisptr
        grd.selectLine(index)

    def set_cell_text(self, line, column, string):
        """
        Changes the text of cell.

        :param line: The line number of the cell to set

        :param column: The column number of the cell to set

        :param string: The new cell text
        """
        cdef cGrid* grd = <cGrid*>self.thisptr
        cdef char* encoded_string
        encoded_string_temporary = string.encode('utf-8')
        encoded_string = encoded_string_temporary
        grd.setCellText(line, column, sfString(encoded_string))

    def set_cell_score_value(self, line, column, score, nb_digits=7,
                             nb_decimals=2):
        """
        Changes the text of cell.

        :param line: The line number of the cell to set

        :param column: The column number of the cell to set

        :param string: The new cell text
        """
        cdef cGrid*grd = <cGrid*> self.thisptr
        grd.setCellScoreValue(line, column, score, nb_digits, nb_decimals)

    def get_cell_text(self, line, column):
        """
        Gets the text of a cell of the grid

        :param line: The line number of the cell to get

        :param column: The line number of the cell to get

        :return The cell text
        """
        cdef cGrid* grd = <cGrid*>self.thisptr
        cdef char* decoded_string
        decoded_string = <char*>grd.getCellText(
            line, column).toAnsiString().c_str()
        return decoded_string.decode('utf-8')

    def set_cell_color(self, line, column, Color color):
        """
        Changes the color of a cell

        :param line: The line number of the cell to set

        :param column: The column number of the cell to set

        :param color: The new cell color
        """
        cdef cGrid* grd = <cGrid*>self.thisptr
        grd.setCellColor(line, column,
                         sfColor(color.r, color.g, color.b, color.a))

    def set_row_texts(self, row, strings):
        """
        Sets the texts of an entire row

        :param row: Index of the row to set

        :param strings: The list of string (one per cell)
        """
        cdef cGrid* grd = <cGrid*>self.thisptr
        cdef char* encoded_string
        cdef vector[sfString] sf_strings
        for string in strings:
            encoded_string_temporary = string.encode('utf-8')
            encoded_string = encoded_string_temporary
            sf_strings.push_back(sfString(encoded_string))
        grd.setRowTexts(row, sf_strings)

    def set_column_texts(self, column, strings):
        """
        Sets the text of an entire column

        :param column: Index of the column to set

        :param strings: The list of string (one per cell)
        """
        cdef cGrid* grd = <cGrid*>self.thisptr
        cdef char* encoded_string
        cdef vector[sfString] sf_strings
        for string in strings:
            encoded_string_temporary = string.encode('utf-8')
            encoded_string = encoded_string_temporary
            sf_strings.push_back(sfString(encoded_string))
        grd.setColumnTexts(column, sf_strings)


#----------------------------------------------------------
# Animations
#----------------------------------------------------------
cdef class TimeLoop(object):
    """
    The TimeLoop class is an utility class for controlling a time loop.

    This class controls the evolution of a normalized value over time. This
    normalized value can then be used to control an animation.

    A normalized value is a floating number clamped between 0 and 1.

    There are a lots of parameters that can be customised:
        - duration: Loop duration
        - frequency: Frequency multiplier
        - phase: Loop phase (time offset)
        - nbIterations: The number of times the loop must be played.
        - direction: Loop direction (forward: 0 -> 1, backward: 1 -> 0)
        - mode: Specify how the loop ends (keep last value or reset)
        - cycle: Play the animation twice with a different direction each time
    """
    # TimeLoop.Mode.Wrap
    #: The control time is reset at the end of the animation
    WRAP = Wrap
    #: The control time is not reset at the end of the animation, it keeps its
    #: last value
    CLAMP = Clamp

    # TimeLoop.Direction
    #: Control time goes upwards (from 0 to duration)
    FORWARD = Forward
    #: Control time goes downwards (from duration to 0)
    BACKWARD = Backward

    cdef cTimeLoop* thisptr

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cTimeLoop()

    def update(self,Time elapsed_time):
        """
        Updates the loop control time
        """
        return self.thisptr.update(elapsed_time.m_time)

    def advance_time(self, Time elapsed_time):
        """
        Advances the control time
        """
        self.thisptr.advanceTime(elapsed_time.m_time)

    def start(self):
        """
        Starts the loop
        """
        self.thisptr.start()

    def stop(self):
        """
        Stops the loop
        """
        self.thisptr.stop()

    def pause(self):
        """
        Pauses the loop
        """
        self.thisptr.pause()

    property duration:
        """
        Gets/Sets the loop duration
        """
        def __get__(self):
            cdef Time t = Time()
            t.m_time = self.thisptr.getDuration()
            return t

        def __set__(self, Time value):
            self.thisptr.setDuration(<sfTime>value.m_time)

    property phase:
        """
        Gets/Sets the loop phase
        """
        def __get__(self):
            cdef Time t = Time()
            t.m_time = self.thisptr.getPhase()
            return t

        def __set__(self, Time value):
            self.thisptr.setPhase(<sfTime>value.m_time)

    property nb_iterations:
        """
        Gets/sets the number of iterations of the loop (min 1)
        """
        def __get__(self):
            return self.thisptr.getNbIterations()

        def __set__(self, value):
            if value < 1:
                value = 1
            self.thisptr.setNbIterations(value)

    property mode:
        """
        Gets/Sets the loop mode
        """
        def __get__(self):
            return self.thisptr.getMode()

        def __set__(self, value):
            self.thisptr.setMode(value)

    property direction:
        """
        Gets/Sets the loop direction
        """
        def __get__(self):
            return self.thisptr.getDirection()

        def __set__(self, value):
            self.thisptr.setDirection(value)

    property cycle:
        """
        Gets/Sets the cylce flag
        """
        def __get__(self):
            return self.thisptr.getCycle()

        def __set__(self, value):
            self.thisptr.setCycle(value)

    property smooth_steps:
        """
        Gets/Sets smooth steps
        """
        def __get__(self):
            return self.thisptr.getSmoothSteps()

        def __set__(self, value):
            self.thisptr.setSmoothSteps(value)

    property control_time:
        """
        Gets the loop control time. This propriety is read only
        """
        def __get__(self):
            cdef Time t = Time()
            t.m_time = self.thisptr.getControlTime()
            return t

    property normalized_control_time:
        """
        Gets the control time as a normalized value [0-1]
        """
        def __get__(self):
            return self.thisptr.getNormalizedControlTime()

    property is_running:
        """
        Gets is running flag value
        """
        def __get__(self):
            return self.thisptr.isRunning()

    property iteration_counter:
        """
        Gets the loop iteration counter
        """
        def __get__(self):
            return self.thisptr.getIterationCounter()

    def reset(self):
        """
        Resets the loop properties
        """
        self.thisptr.reset()

    def revert_direction(self):
        """
        Revert the loop direction
        """
        self.thisptr.revertDirection()


#----------------------------------------------------------
cdef class Animation(_Disown):
    """
    An animation uses a TimeLoop to controls a target property, the type of
    the target and the controlled property is specific to a concrete animation,
    eg some animation will target any kind of game item while some other
    animation will only deal with a specific kind of game item.

    Concrete animations must implement the specific update method and provides
    a way for the user to specify the animation target.

    For most animations, you will have to configure the internal time loop.
    Most of the animation signals (finished, iterationFinished) are defined in
    the time loop object.

    You can do that acces the internal time loop using the Animation::timeLoop
    method wich returns a modifiable pointer to the internal loop. The animation
    alos exposed the most important functions of the time loop

    Here is a short example that shows how to use most of the animation classes:
    .. codeblock: python

        anim.time_loop.duration = gterm.Time.from_seconds(2.34)
        # is the same as
        anim.duration = gterm.Time.from_seconds(2.34)
        # run the anim
        anim.start()


    .. note:: All animations should be instanciated using the anim_define_xxx
              functions where xxx is the name of the animation type
              (anim_define_rotation, anim_define_scale, ...)

    .. note:: This base class can be used as a timer.

    """
    cdef cAnimation* thisptr

    cdef object __finished_func
    cdef object __it_finished_func

    #: Signal emitted when the animation finished (when all iteration completed)
    cdef public Signal finished
    #: Signal emitted at the end of a loop iteration
    cdef public Signal iteration_finished

    def __cinit__(self, *args, **kargs):
        self.finished = Signal()
        self.iteration_finished = Signal()
        self.thisptr = new cAnimation()

    def __init__(self):
        _Disown.__init__(self)
        self._init_callbacks()

    def __dealloc__(self):
        if not self._disown:
            del self.thisptr

    property is_running:
        """
        Checks if the animation is running
        """
        def __get__(self):
            return self.thisptr.isRunning()

    property name:
        """
        Gets/Sets the name of the animation
        """
        def __get__(self):
            return self.thisptr.getName()

        def __set__(self, value):
            self.thisptr.setName(value)

    property duration:
        """
        Gets/Sets the duration of the internal time loop
        """
        def __get__(self):
            cdef Time t = Time()
            t.m_time = self.thisptr.getDuration()
            return t

        def __set__(self, Time value):
            self.thisptr.setDuration(<sfTime>value.m_time)

    property phase:
        """
        Gets/sets phase of the internal time loop
        """
        def __get__(self):
            cdef Time t = Time()
            t.m_time = self.thisptr.getPhase()
            return t

        def __set__(self, Time value):
            self.thisptr.setPhase(<sfTime>value.m_time)

    property nb_iterations:
        """
        Gets/Sets the number of iteration of the internal time loop
        """
        def __get__(self):
            return self.thisptr.getNbIterations()

        def __set__(self, value):
            self.thisptr.setNbIterations(value)

    property mode:
        """
        Gets/Sets the mode of the internal time loop
        """
        def __get__(self):
            return self.thisptr.getMode()

        def __set__(self, value):
            self.thisptr.setMode(value)

    property direction:
        """
        Gets/Sets the direction of the internal time loop
        """
        def __get__(self):
            return self.thisptr.getDirection()

        def __set__(self, value):
            self.thisptr.setDirection(value)

    property cycle:
        """
        Gets/Sets the cycle flag of the internal time loop
        """
        def __get__(self):
            return self.thisptr.getCycle()

        def __set__(self, value):
            self.thisptr.setCycle(value)

    property smooth_steps:
        """
        Gets/sets the smoot_steps flag of the internal time loop
        """
        def __get__(self):
            return self.thisptr.getSmoothSteps()

        def __set__(self, value):
            self.thisptr.setSmoothSteps(value)

    property time_loop:
        """
        Gets a reference to the internal time loop
        """
        def __get__(self):
            cdef cTimeLoop* tl = self.thisptr.timeLoop()
            if tl == NULL:
                return None
            cdef TimeLoop ret_val = TimeLoop()
            del ret_val.thisptr
            ret_val.thisptr = tl
            return ret_val

    def update(self, Time t):
        """
        Updates the animation

        :param t: Elapsed time since the last frame
        """
        self.thisptr.update(t.m_time)

    def start(self):
        """
        Starts the animation
        """
        self.thisptr.start()

    def stop(self):
        """
        Stops the animation
        """
        self.thisptr.stop()

    def pause(self):
        """
        Pauses the animation
        """
        self.thisptr.pause()

    def _init_callbacks(self):
        """
        Inits the internal callbacks to automatically emits the corresponding
        python signals
        """
        self.thisptr.__cy__setFinishedCallback(__callback,
                                               <void*>self._on_finished)
        self.__finished_func = self._on_finished
        self.thisptr.__cy__setIterationFinishedCallback(
            __callback, <void*>self._on_iteration_finished)
        self.__it_finished_func = self._on_iteration_finished

    def _on_finished(self):
        """
        Emits the finished signal
        """
        self.finished()

    def _on_iteration_finished(self):
        """
        Emits the iteration_finished signal
        """
        if self.time_loop:
            self.iteration_finished(self.time_loop.iteration_counter)
        else:
            self.iteration_finished(INFINITE)

    def _link_events(self):
        self.thisptr.linkTimeLoopEvents()


class Timer(Animation):
    def __init__(self, name, interval=Time().from_seconds(1.0), infinite=False):
        Animation.__init__(self)
        self._link_events()
        self._init_callbacks()
        self.name = name
        self.timeout = Signal()
        self.interval = interval
        self.iteration_finished.connect(self.__on_timeout)
        if infinite:
            self.nb_iterations = INFINITE
        else:
            self.nb_iterations = 1

    @property
    def interval(self):
        return self.duration

    @interval.setter
    def interval(self, value):
        self.duration = value

    def __on_timeout(self, *args, **kargs):
        self.timeout()

#----------------------------------------------------------
cdef class AnimationBlink(Animation):
    """
    The AnimationBlink class animates the visibility of a GameItem.

    The blink animation defines the following additional parameters:
        - duty cyle: ration between Toff and Ton
        - start state: The visibility start state (hidden or shown)
        - target: the target game item

    .. warning:: To create a AnimationBlink you **MUST** use the
                 anim_define_blink function
    """
    def __cinit__(self, *args, **kargs):
        self.thisptr = new cAnimationBlink()

    def __init__(self, name, duty_cycle=0.5, start_state=False):
        Animation.__init__(self)
        self.thisptr.setName(name)
        cdef cAnimationBlink* blk = <cAnimationBlink*>self.thisptr
        blk.setDutyCycle(duty_cycle)
        blk.setStartState(start_state)

    property duty_cycle:
        """
        Gets/Sets the blink duty cycle
        """
        def __get__(self):
            cdef cAnimationBlink* blk = <cAnimationBlink*>self.thisptr
            return blk.getDutyCycle()

        def __set__(self, dt):
            cdef cAnimationBlink* blk = <cAnimationBlink*>self.thisptr
            blk.setDutyCycle(dt)

    property start_state:
        """
        Gets/Sets the visibility state used when starting the animation
        """
        def __get__(self):
            cdef cAnimationBlink* blk = <cAnimationBlink*>self.thisptr
            return blk.getStartState()

        def __set__(self, bool value):
            cdef cAnimationBlink* blk = <cAnimationBlink*>self.thisptr
            blk.setStartState(value)

    property current_state:
        """
        Gets the currents visibility state (true= shown, false=hidden)
        """
        def __get__(self):
            cdef cAnimationBlink* blk = <cAnimationBlink*>self.thisptr
            return blk.getCurrentState()


#----------------------------------------------------------
def anim_define_blink(GameItem2D target,
                      name="blinker",
                      Time duration = Time().from_seconds(1.0),
                      float duty_cycle=0.5,
                      bool start_state=False):

    """
    Creates a blink animation and adds it to the specified target

    :param target: The target game item

    :param name: The animation name

    :param duration: The duration of the animation

    :param duty_cycle: The blink duty cycle

    :param start_state: The blink start state

    :return: An animation blink already configured
    :rtype: AnimationBlink
    """
    cdef cAnimationBlink* anim = animDefineBlink(
        <cGameItem*> target.thisptr, name, duration.m_time, duty_cycle,
        start_state)
    cdef AnimationBlink retval = AnimationBlink("")
    del retval.thisptr
    retval.thisptr = anim
    retval._disown = True
    retval._init_callbacks()
    target._setattr(name, retval)
    return retval


#----------------------------------------------------------
cdef class AnimationFade(Animation):
    """
    The AnimationFade class animates the opacity of the target game item.

    Opacity will vary from opacity min to opacity max or inversely depending
    on the fade type.

    .. warning:: To create a AnimationFade you **MUST** use the
                 anim_define_fade function
    """
    # AnimationFade.FadeType enum
    #: Opacity goes from min to max
    FADE_IN = FadeIn
    #: Opacity goes from max to min
    FADE_OUT = FadeOut

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cAnimationFade()

    property opacity:
        """
        Gets the current opacity value
        """
        def __get__(self):
            cdef cAnimationFade* anim = <cAnimationFade*>self.thisptr
            return anim.getOpacity()

    property opacity_min:
        """
        Gets/Sets the opacity min value
        """
        def __get__(self):
            cdef cAnimationFade* anim = <cAnimationFade*>self.thisptr
            return anim.getOpacityMin()

        def __set__(self, value):
            cdef cAnimationFade* anim = <cAnimationFade*>self.thisptr
            anim.setOpacityMin(value)

    property opacity_max:
        """
        Gets/Sets the opacity max value
        """
        def __get__(self):
            cdef cAnimationFade* anim = <cAnimationFade*>self.thisptr
            return anim.getOpacityMax()

        def __set__(self, value):
            cdef cAnimationFade* anim = <cAnimationFade*>self.thisptr
            anim.setOpacityMax(value)

    property fade_type:
        """
        Gets/Sets the fade type
        """
        def __get__(self):
            cdef cAnimationFade* anim = <cAnimationFade*>self.thisptr
            return anim.getFadeType()

        def __set__(self, value):
            cdef cAnimationFade* anim = <cAnimationFade*>self.thisptr
            anim.setFadeType(value)

    def set_state(self, fade_type):
        """
        Immediately change the target game item opacity depending on the fade
        type. If fade_in the target opacity is set to opacity_max, else it is
        set to opacity_min
        """
        cdef cAnimationFade* anim = <cAnimationFade*>self.thisptr
        anim.setState(fade_type)


#----------------------------------------------------------
def anim_define_fade(GameItem2D target,
                     name="fader",
                     Time duration = Time().from_seconds(1.0),
                     float opacity_min=0,
                     float opacity_max=1,
                     fade_type = AnimationFade.FADE_IN,
                     mode = TimeLoop.CLAMP):
    """
    Helper functions that creates an AnimationFade and set it on the
    target game item

    :param target: Animation target
    :param name: Animation name
    :param duration: Animation duration
    :param opacity_min: Opacity min
    :param opacity_max: Opacity max
    :param fade_type: Fade type

    :rtype : AnimationFade
    """
    cdef cAnimationFade* anim = animDefineFade(
        <cGameItem*> target.thisptr, name, duration.m_time,
        opacity_min, opacity_max, fade_type, mode)
    cdef AnimationFade retval = AnimationFade()
    del retval.thisptr
    retval.thisptr = anim
    retval._disown = True
    retval._init_callbacks()
    target._setattr(name, retval)
    return retval


#----------------------------------------------------------
cdef class AnimationRotation(Animation):
    """
    The AnimationTranslation class animates the orientation of a game item.
    """
    def __cinit__(self, *args, **kargs):
        self.thisptr = new cAnimationRotation()

    property rotation:
        """
        Gets/sets the animation rotation.

        The rotation is always returned as a tuple of float (x, y, z)

        To set the rotation you may use a tuple of float for a 3D rotation, a
        single float for a 2D rotation
        """
        def __get__(self):
            cdef cAnimationRotation* anim = <cAnimationRotation*>self.thisptr
            cdef Vector3f v = anim.getRotation()
            return v.x, v.y, v.z

        def __set__(self, value):
            cdef cAnimationRotation* anim = <cAnimationRotation*>self.thisptr
            if isinstance(value, float) or isinstance(value, int):
                anim.setRotation(Vector3f(0, 0, value))
            else:
                anim.setRotation(Vector3f(value[0], value[1], value[2]))


#----------------------------------------------------------
def anim_define_rotation(GameItem2D target,
        name,
        rotation,
        Time duration,
        mode=TimeLoop.CLAMP,
        bool smooth_steps=True):
    """
    Helper functions that setups a rotation animation on the target game item.

    :param target: The target game item
    :param name: The anim name
    :param rotation: The anim rotation vector (tuple of 3 floats -> 3d) or
                     the animation angle (float -> 2d)
    :param duration: The anim duration
    :param mode: The anim mode
    :param smooth_steps: Smoothsteps flag

    :rtype: AnimationRotation
    """
    cdef cAnimationRotation* anim = NULL
    if isinstance(rotation, float) or isinstance(rotation, int):
        anim = animDefineRotation(<cGameItem*> target.thisptr, name,
                                  Vector3f(0, 0, rotation),
                                  duration.m_time,
                                  mode,
                                  smooth_steps)
    else:
        anim = animDefineRotation(<cGameItem*> target.thisptr, name,
                                  Vector3f(rotation[0],
                                           rotation[1],
                                           rotation[2]),
                                  duration.m_time,
                                  mode,
                                  smooth_steps)
    cdef AnimationRotation retval = AnimationRotation()
    del retval.thisptr
    retval.thisptr = anim
    retval._disown = True
    retval._init_callbacks()
    target._setattr(name, retval)
    return retval


#----------------------------------------------------------
cdef class AnimationTranslation(Animation):
    """
    The AnimationTranslation class animates the position of a game item.
    """
    def __cinit__(self, *args, **kargs):
        self.thisptr = new cAnimationTranslation()

    property translation:
        """
        Gets/sets the animation position.

        The position is always returned as a tuple of float (x, y, z)

        To set the position you may use a tuple of 3 float/int for a 3D
        rotation or a tuple of 2 float/int for a 2D rotation.
        """
        def __get__(self):
            cdef cAnimationTranslation* anim = \
                <cAnimationTranslation*>self.thisptr
            cdef Vector3f v = anim.getTranslation()
            return v.x, v.y, v.z

        def __set__(self, value):
            cdef cAnimationTranslation* anim = \
                <cAnimationTranslation*>self.thisptr
            if type(value) is tuple:
                if len(value) == 2:
                    anim.setTranslation(value[0], value[1], 0)
                else:
                    anim.setTranslation(value[0], value[1], value[2])
            else:
                raise TypeError("Translation must be a tuple of 2 or 3 "
                                "float/int")


#----------------------------------------------------------
def anim_define_translation(GameItem2D target, name, translation, Time duration,
                            mode=TimeLoop.CLAMP, bool smooth_steps=True):
    """
    Helper functions that setups a translation animation on the target game
    item.

    :param target: The target game item
    :param name: The anim name
    :param translation: The anim translation vector (tuple of 3 floats -> 3d or
                        tuple of 2 floats -> 2d)
    :param duration: The anim duration
    :param mode: The anim mode
    :param smooth_steps: Smoothsteps flag

    :rtype: AnimationTranslation
    """
    cdef cAnimationTranslation* anim = NULL
    if type(translation) is tuple:
        if len(translation) == 2:
            anim = animDefineTranslation(<cGameItem*> target.thisptr, name,
                                         Vector3f(translation[0],
                                                  translation[1],
                                                  0),
                                         duration.m_time, mode, smooth_steps)
        else:
            anim = animDefineTranslation(<cGameItem*> target.thisptr, name,
                                         Vector3f(translation[0],
                                                  translation[1],
                                                  translation[2]),
                                         duration.m_time, mode, smooth_steps)
    else:
        raise TypeError("Translation must be a tuple of 2 or 3 "
                        "float/int")
    cdef AnimationTranslation retval = AnimationTranslation()
    del retval.thisptr
    retval.thisptr = anim
    retval._disown = True
    retval._init_callbacks()
    target._setattr(name, retval)
    return retval


#----------------------------------------------------------
cdef class AnimationScale(Animation):
    """
    The AnimationScale class animates the scale of a game item.
    """
    def __cinit__(self, *args, **kargs):
        self.thisptr = new cAnimationScale()

    property scale:
        """
        Gets/sets the animation scale.

        The scale is always returned as a tuple of float (x, y, z)

        To set the scale you may use a tuple of 3 float/int for a 3D
        scale, a tuple of 2 float/int for a 2D scale or a single float for
        an uniform scale (2d or 3d).
        """
        def __get__(self):
            cdef cAnimationScale* anim = <cAnimationScale*>self.thisptr
            cdef Vector3f v = anim.getScale()
            return v.x, v.y, v.z

        def __set__(self, value):
            cdef cAnimationScale* anim = <cAnimationScale*>self.thisptr
            if type(value) is tuple:
                if len(value) == 2:
                    anim.setScale(Vector3f(value[0], value[1], 1))
                else:
                    anim.setScale(Vector3f(value[0], value[1], value[2]))
            elif isinstance(value, float) or isinstance(value, int):
                anim.setScale(Vector3f(value, value, value))
            else:
                raise TypeError("Scale must be a tuple of 2 or 3 "
                                "float/int or a single float/int")


#----------------------------------------------------------
def anim_define_scale(GameItem2D target, name, scale,
                      Time duration=Time().from_seconds(1),
                      mode=TimeLoop.CLAMP, bool smooth_steps=True):
    """
    Helper functions that setups a scale animation on the target game
    item.

    :param target: The target game item
    :param name: The anim name
    :param scale: The anim scale vector (tuple of 3 floats -> 3d or
                        tuple of 2 floats -> 2d or a float -> uniform scale)
    :param duration: The anim duration
    :param mode: The anim mode
    :param smooth_steps: Smoothsteps flag

    :rtype: AnimationTranslation
    """
    cdef cAnimationScale* anim = NULL
    if type(scale) is tuple:
        if len(scale) == 2:
            anim = animDefineScale(<cGameItem*> target.thisptr, name,
                                   Vector3f(scale[0],
                                            scale[1],
                                            1),
                                   duration.m_time, mode, smooth_steps)
        else:
            anim = animDefineScale(<cGameItem*> target.thisptr, name,
                                   Vector3f(scale[0],
                                            scale[1],
                                            scale[2]),
                                   duration.m_time, mode, smooth_steps)
    elif isinstance(scale, float) or isinstance(scale, int):
        anim = animDefineScale(<cGameItem*> target.thisptr, name,
                               Vector3f(scale, scale, scale),
                               duration.m_time, mode, smooth_steps)
    else:
        raise TypeError("Translation must be a tuple of 2 or 3 "
                        "float/int")
    cdef AnimationScale retval = AnimationScale()
    del retval.thisptr
    retval.thisptr = anim
    retval._disown = True
    retval._init_callbacks()
    target._setattr(name, retval)
    return retval


#----------------------------------------------------------
cdef class AnimationTexture(Animation):
    """
    The AnimationTexture class animates the texture of a sprite.

    The animation texture consists in a list of texture associated with a
    duration. The animation cycle through the list of texture and display
    each one on the target sprite during the specified duration.


    .. note:: The internal time loop is used as a timer for each texture step
              and should not be set externally, that's why we override the
              time_loop property method to always return a None.
    """
    cdef object _index_changed_fct
    cdef public Signal index_changed

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cAnimationTexture()
        self.index_changed = Signal()

    def __init__(self, name):
        Animation.__init__(self)
        self.thisptr.setName(name)
        self._init_index_callback()

    property is_running:
        """
        Checks if the animation is running
        """
        def __get__(self):
            cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
            return anim.isRunning()

    property nb_iterations:
        """
        Gets/Sets the number of iteration of the internal time loop
        """
        def __get__(self):
            cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
            return anim.getNbIterations()

        def __set__(self, value):
            cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
            anim.setNbIterations(value)

    property reverse:
        """
        Gets/Sets the reverse flag
        """
        def __get__(self):
            cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
            return anim.isReverse()

        def __set__(self, value):
            cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
            anim.setReverse(value)

    property current_index:
        """
        Gets/Sets the current texture index
        """
        def __get__(self):
            cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
            return anim.getCurrentIndex()

        def __set__(self, value):
            cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
            anim.setCurrentIndex(value)

    property end_index:
        """
        Gets/sets the end texture index
        """
        def __get__(self):
            cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
            return anim.getEndIndex()

        def __set__(self, value):
            cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
            anim.setEndIndex(value)

    property count:
        """
        Gets the number of textures in the sequence
        """
        def __get__(self):
            cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
            return anim.count()

    def add_texture(self, filename, Time duration=Time().from_milliseconds(16)):
        """
        Adds a texture to the sequence

        :param filename: The filename of the texture to add

        :param duration: The texture duration
        """
        cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
        anim.addTexture(filename, duration.m_time)

    def clear(self):
        """
        Removes all textures from the sequence
        """
        cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
        anim.clear()

    def _init_index_callback(self):
        """
        Init index callback
        """
        cdef cAnimationTexture* anim = <cAnimationTexture*>self.thisptr
        anim.__cy__setIndexChangedCallback(
            __callback, <void*>self._on_index_changed)
        self._index_changed_fct = self._on_index_changed

    def _on_index_changed(self):
        """
        Emits the index changed signal
        """
        self.index_changed(self.current_index)


#----------------------------------------------------------
def anim_define_texture_anim(
        GameItem2D target, name, texture_base="",
        nb_textures=0, Time duration=Time().from_microseconds(16)):
    """
    Helper function to define a texture animation

    :param target: The target game item (Must be a Texturable)
    :param name: The animation name
    :param texture_base: The base texture filename. Optional
    :param nb_textures: Number of textures to add. Only required if texture_base
                        is not an empty string
    :param duration: The textures duration. Only required if texture_base
                     is not an empty string

    :return: AnimationTexture
    """
    cdef cAnimationTexture* anim = animDefineTextureAnim(
        <cGameItem*> target.thisptr, name, texture_base, nb_textures,
        duration.m_time)
    cdef AnimationTexture retval = AnimationTexture("")
    del retval.thisptr
    retval.thisptr = anim
    retval._disown = True
    retval._init_callbacks()
    retval._init_index_callback()
    target._setattr(name, retval)
    return retval


#----------------------------------------------------------
def anim_load_texture_anim(
        GameItem2D target, filename, name="texture_anim"):
    """
    Helper function to define a texture animation

    :param target: The target game item (Must be a Texturable)
    ;param filename: The animation filename
    :param name: The animation name

    :return: AnimationTexture
    """
    cdef cAnimationTexture* anim = animLoadTextureAnim(
        <cGameItem*> target.thisptr, filename, name)
    cdef AnimationTexture retval = AnimationTexture("")
    del retval.thisptr
    retval.thisptr = anim
    retval._disown = True
    retval._init_callbacks()
    retval._init_index_callback()
    target._setattr(name, retval)
    return retval


#----------------------------------------------------------
# Helpers
#----------------------------------------------------------
cdef class ZoneFile(object):
    cdef cZoneFile* thisptr

    def __cinit__(self, *args, **kargs):
        self.thisptr = NULL

    def has_zone(self, zone_color):
        """
        Checks if the zone file contains a specific zone

        :param zone_color: The color of the zone

        :return True if the zone exists, else False
        :rtype bool
        """
        return self.thisptr.hasZone(zone_color)

    def get_center_position(self, zone_color):
        """
        Gets the center position of the specified zone

        :param zone_color: The color of the zone

        :return The zone position (tuple of int)
        """
        ret = self.thisptr.getCenterPosition(zone_color)
        return ret.x, ret.y

    def get_corner_position(self, zone_color):
        """
        Gets the corner position of the specified zone

        :param zone_color: The color of the zone

        :return The zone position (tuple of int)
        """
        ret = self.thisptr.getCornerPosition(zone_color)
        return ret.x, ret.y

    def get_relative_center_pos(self, zone_color):
        ret = self.thisptr.getRelativeCenterPosition(zone_color)
        return ret.x, ret.y

    def get_size(self, zone_color):
        """
        Gets the size of the specified zone

        :param zone_color: The color of the zone

        :return The zone size (tuple of int)
        """
        ret = self.thisptr.getSize(zone_color)
        return ret.x, ret.y

    def get_zone_rect(self, zone_color):
        cdef sfIntRect sfRect = self.thisptr.getZoneRect(zone_color)
        cdef IntRect r = IntRect()
        r.m_rect = sfRect
        return r

    property size:
        """
        Gets the size of the zone file (size of the whole image)
        """
        def __get__(self):
            ret = self.thisptr.getImageSize()
            return ret.x, ret.y

    property colors:
        """
        Gets the list of zone colors
        """
        def __get__(self):
            return self.thisptr.getColors()

def get_zone_file(filename):
    """
    Gets a zone file from name.

    :param filename: Zone filename

    :rtype ZoneFile
    """
    cdef ZoneFile zf = ZoneFile()
    zf.thisptr = __cy__getZoneFile(filename)
    if zf.thisptr == NULL:
        return None
    else:
        return zf


cdef class ConfigFile(object):
    """
    Utility class to load a gterm config file.
    """
    cdef cConfigFile thisptr

    def __cinit__(self, *args, **kargs):
        self.thisptr = cConfigFile()

    def load(self, filename):
        """
        Loads the config file
        """
        return self.thisptr.load(filename)

    def value(self, key):
        """
        Gets a string value
        """
        return self.thisptr.value(key)

    def value_as_bool(self, filename):
        """
        Gets a bool value
        """
        return self.thisptr.valueAsBool(filename)

    def value_as_int(self, filename):
        """
        Gets an int value
        """
        return self.thisptr.valueAsInt(filename)

    def value_as_float(self, filename):
        """
        Gets a float value
        """
        return self.thisptr.valueAsFloat(filename)

    def value_as_vector2(self, filename):
        """
        Gets a vector2 value, returned as a tuple of float
        """
        ret = self.thisptr.valueAsVector2(filename)
        return ret.x, ret.y


#----------------------------------------------------------
# RPC
#----------------------------------------------------------
cdef class RpcStack(object):
    """
    The RpcStack class is a LIFO that stores data from an Rpc frame.

    Only contains the data part of a RPC frame (does not contains command id,
    checksum and frame size).
    """
    cdef cRpcStack thisptr

    def flush(self):
        """
        Flushes the data stack
        """
        self.thisptr.flush()

    def push_byte(self, value):
        """
        Pushes a byte on top of the stack
        """
        self.thisptr.pushByte(value)

    def push_word(self, value):
        """
        Pushes a word on top of the stack
        """
        self.thisptr.pushWord(value)

    def push_long(self, value):
        """
        Pushes a long on top of the stack
        """
        self.thisptr.pushLong(value)

    def pop_byte(self):
        """
        Pops a byte from the top of the stack
        """
        return self.thisptr.popByte()

    def pop_word(self):
        """
        Pops a byte from the top of the stack
        """
        return self.thisptr.popWord()

    def pop_long(self):
        """
        Pops a byte from the top of the stack
        """
        return self.thisptr.popLong()

    property nb_in:
        """
        Gets the number of bytes in the data stack
        """
        def __get__(self):
            return self.thisptr.getNbIn()

    property is_empty:
        """
        Gets empty stack flag value
        """
        def __get__(self):
            return self.thisptr.isEmpty()

    property checksum:
        """
        Gets the checksum of the data stack
        """
        def __get__(self):
            return self.thisptr.checksum()

    def __repr__(self):
        return self.thisptr.toString()

    def __str__(self):
        return self.thisptr.toString()


cdef class RpcFrame(object):
    """
    Contains the data needed for an rpc frame:
        - id
        - nb_bytes
        - data (RpcStack)
        - checksum.

    .. warning:: The default ctor is empty. To create a frame from a stack and an
              id, use the classmethod create!
    """
    cdef cRpcFrame thisptr

    def __cinit__(self, *args, **kargs):
        self.thisptr = cRpcFrame()

    @classmethod
    def create(cls, id, RpcStack stack):
        """
        Creates an rpc frame from an id and a data stack

        :rtype pyGTerm.gterm.RpcFrame
        """
        cdef RpcFrame f = RpcFrame()
        cdef cRpcFrame cf = cRpcFrame(id, stack.thisptr)
        f.thisptr = cf
        return f

    property checksum:
        """
        Gets the frame checksum.
        """
        def __get__(self):
            return self.thisptr.checksum()

    property id:
        """
        Gets the command id
        """
        def __get__(self):
            return self.thisptr.id()

    property nb_bytes:
        """
        Gets the number of bytes contained in the frame
        """
        def __get__(self):
            return self.thisptr.nbBytes()

    property data:
        """
        Gets the data stack
        """
        def __get__(self):
            cdef RpcStack s = RpcStack()
            s.thisptr = self.thisptr.getDatas()
            return s

    def __repr__(self):
        return self.thisptr.toString()

    def __str__(self):
        return self.thisptr.toString()


cdef class RpcParameter(object):
    """
    Te RpcParameter class represent an rpc command parameter.

    A parameter is identifier by a name, a type and an optional description.
    """
    cdef cRpcParameter* m_param

    def __cinit__(self, name, pa_type, desc):
        self.m_param = new cRpcParameter(name, pa_type, desc)

    property name:
        """
        Gets/Sets the parameter name
        """
        def __get__(self):
            return self.m_param.getName().decode("latin-1")

        def __set__(self, value):
            self.m_param.setName(value.encode("latin-1"))

    property type:
        """
        Gets/Sets the parameter type (byte, word or long)
        """
        def __get__(self):
            return self.m_param.getType()

        def __set__(self, value):
            self.m_param.setType(value)

    property description:
        """
        Gets/Sets the parameter description
        """
        def __get__(self):
            return self.m_param.getDescription().decode("latin-1")

        def __set__(self, value):
            self.m_param.setDescription(value.encode("latin-1"))


cdef class RpcCommand(object):
    """
    RpcCommand represents an rpc command definition:
     - id
     - name
     - description
     - list of parameters
    """
    cdef cRpcCommand* m_cmd

    def __cinit__(self, name, id, desc="", protected=True):
        self.m_cmd = new cRpcCommand(name, id, desc, protected)

    property name:
        """
        Gets/Sets the command name
        """
        def __get__(self):
            return self.m_cmd.getName().decode("latin-1")

        def __set__(self, value):
            self.m_cmd.setName(value.encode("latin-1"))

    property id:
        """
        Gets/Sets the command id
        """
        def __get__(self):
            return self.m_cmd.getId()

        def __set__(self, value):
            self.m_cmd.setId(value)

    def add_parameter(self, RpcParameter param):
        """
        Addsa a parameter to the command
        """
        return self.m_cmd.addParameter(deref(param.m_param))

    def remove_parameter(self, index):
        """
        Removes a parameter from the command

        :param index: Index of the parameter to remove
        """
        self.m_cmd.removeParameter(index)

    property nb_parameters:
        """
        Gets the number of parameters defined in the command
        """
        def __get__(self):
            return self.m_cmd.getNbParameter()

    def get_parameter(self, i):
        """
        Gets the Ith parameter
        """
        cdef RpcParameter p = RpcParameter("", 0, "")
        del p.m_param
        p.m_param = self.m_cmd.getParameter(i)
        return p

    def check(self, RpcStack stack):
        """
        Checks if a data stack match the command definition
        """
        return self.m_cmd.check(stack.thisptr)

    property pending:
        """
        Gets/Sets the pending flag
        """
        def __set__(self, value):
            self.m_cmd.setPending(value)

        def __get__(self):
            return self.m_cmd.isPending()

    property protected:
        """
        Gets/Sets the protected flag
        """
        def __get__(self):
            return self.m_cmd.isProtected()

        def __set__(self, value):
            self.m_cmd.setProtected(value)

    property description:
        """
        Gets/Sets the command description
        """
        def __set__(self, value):
            self.m_cmd.setDescription(value.encode("latin-1"))

        def __get__(self):
            return self.m_cmd.getDescription().decode("latin-1")

    def __repr__(self):
        retval = "{0} ({1}): {2}".format(self.name, self.id, self.description)
        for i in range(self.nb_parameters):
            p = self.get_parameter(i)
            retval += "\n\t-{0} ({1}): {2}".format(
                p.name, param_type_to_string(p.type), p.description)
        return retval


cdef class RpcHandler(object):
    """
    An rpc handler is an utility class that MUST be used to connect a slot to a
    command signal (receive and abort).

    To use this class, you must pass it the desired command id and a callable
    object (= slot). The abort slot is optional as most of the methods does not
    need to be aborted.
    """
    cdef CyRpcHandler* thisptr
    cdef object __rcv_func
    cdef object __abort_func
    cdef object __rcv_slot
    cdef object __abort_slot

    def __cinit__(self, unsigned int cmdId, rcv_slot, abort_slot=None):
        self.thisptr = new CyRpcHandler(cmdId)

    def __init__(self, unsigned int cmdId, rcv_slot, abort_slot=None):
        """
        Creates an rpc handler

        :param cmdId: The command id to handle

        :param rcv_slot: The slot called when the specified command is received

        :param abort_slot: The slot that is called when the specified command is
                           aborted. Optional.
        """
        self.__set_receive_callback(self.on_receive)
        self.__set_abort_callback(self.on_abort)
        self.__rcv_slot = rcv_slot
        self.__abort_slot = abort_slot

    def __set_receive_callback(self, func):
        self.thisptr.__cy__setReceiveCallback(__callback, <void*>func)
        self.__rcv_func = func

    def __set_abort_callback(self, func):
        self.thisptr.__cy__setAbortCallback(__callback, <void*>func)
        self.__abort_func = func

    def on_receive(self):
        """
        Calls the slot.

        .. note:: The command arguments are automatically unpacked based on the
                  command definition. If you have a command that receives a byte
                  and a words, you will have to connect a slot with the same
                  signature::

                        def myCmd(self, byte_param, word_param)
        """
        def extract_raw(RpcStack stack, remain=0):
            str = ""
            char_array = [ ]
            while stack.nb_in > remain:
                char_array.append(chr(stack.pop_byte()))
            for c in reversed( char_array ):
                str += c
            return str
        cdef RpcParameter p
        cdef RpcStack s = RpcStack()
        # extract parameters
        s.thisptr = self.thisptr.getStack()
        cdef RpcCommand command = Application.get_command(self.thisptr.cmdId())
        cdef list params = []
        cdef object param
        for i in reversed(range(command.nb_parameters)):
            p = command.get_parameter(i)
            if p.type == PA_BYTE:
                param = s.pop_byte()
            elif p.type == PA_WORD:
                param = s.pop_word()
            elif p.type == PA_LONG:
                param = s.pop_long()
            else:
                param = extract_raw(s)
            params.append(param)
        params.reverse()
        # call slot
        retVal = self.__rcv_slot(*params)

        # affect results
        if not retVal:
            retVal = RpcStatus.DELAYED
        self.thisptr.setResult(retVal)

    def on_abort(self):
        if self.__abort_slot:
            self.__abort_slot()


cdef class TcpTerminalClient(object):
    """
    Exposes the TcpTerminalClient, a tcp terminal specifically designed for
    the client application( typically the RPCEmulator built into the
    GTermEditor)
    """
    cdef cTcpTerminalClient* thisptr

    def __cinit__(self, *args, **kargs):
        self.thisptr = new cTcpTerminalClient()

    def connect(self, ip_address, port):
        """
        Connects the ip_address on the specified port.

        :param ip_address: The remote ip_address

        :param port; The remote port
        """
        return self.thisptr.connect(ip_address, port)

    def disconnect(self):
        """
        Disconnects from the server
        """
        return self.thisptr.disconnect()

    def send(self, RpcFrame frame):
        """
        Sends an rpc frame to the server
        """
        self.thisptr.send(frame.thisptr)

    def collect_frames(self):
        """
        Collect incoming rpc frames
        """
        self.thisptr.collectFrames()

    def pop(self):
        """
        Pop a collected frame
        """
        cdef RpcFrame f = RpcFrame()
        f.thisptr = self.thisptr.popCommand()
        return f

    def has_commands(self):
        """
        Checks if there are incoming command that needs to handled.
        """
        return self.thisptr.hasCommands()

    def map_command_name(self, id, name):
        """
        Map a command id with its name for an easier debugging
        """
        self.thisptr.mapCommandName(id, name)

    def clear_command_names(self):
        """
        Clears the command name mapping
        """
        self.thisptr.clearCmdNames()

    property is_connected:
        """
        Gets the connected flag value
        """
        def __get__(self):
            return self.thisptr.isConnected()

#----------------------------------------------------------
# SFML classes
#----------------------------------------------------------
cdef class IntRect(object):
    """
    Utility class for manipulating 2D axis aligned rectangles.

    A rectangle is defined by its top-left corner and its size.

    It is a very simple class defined for convenience, so its member variables
     (left, top, width and height) are public and can be accessed directly,
     just like the vector classes (Vector2 and Vector3).

    To keep things simple, sf::Rect doesn't define functions to emulate the
    properties that are not directly members (such as right, bottom, center,
    etc.), it rather only provides intersection functions.

    sf::Rect uses the usual rules for its boundaries:

    The left and top edges are included in the rectangle's area
    The right (left + width) and bottom (top + height) edges are excluded from
    the rectangle's area
    This means that sf::IntRect(0, 0, 1, 1) and sf::IntRect(1, 1, 1, 1)
    don't intersect.

    sf::Rect is a template and may be used with any numeric type, but for
    simplicity the instanciations used by SFML are typedefed:

    sf::Rect<int> is sf::IntRect -> gterm.IntRect
    """
    cdef sfIntRect m_rect

    def __init__(self, left=0, top=0, width=0, height=0):
        self.m_rect.left = left
        self.m_rect.top = top
        self.m_rect.width = width
        self.m_rect.height = height

    def contains(self, point):
        """
        Checks if the rect contains a point
        """
        return self.m_rect.contains(point[0], point[1])

    def contains(self, IntRect rect):
        """
        Checks if the rect contains a point
        """
        return self.m_rect.intersects(rect.m_rect)

    property left:
        """
        The left coordinate
        """
        def __set__(self, value):
            self.m_rect.left = value

        def __get__(self):
            return self.m_rect.left

    property top:
        """
        The top coordinate
        """
        def __set__(self, value):
            self.m_rect.top = value

        def __get__(self):
            return self.m_rect.top

    property width:
        """
        The width of rectangle
        """
        def __set__(self, value):
            self.m_rect.width = value

        def __get__(self):
            return self.m_rect.width

    property height:
        """
        The height of the rectangle
        """
        def __set__(self, value):
            self.m_rect.height = value

        def __get__(self):
            return self.m_rect.height

    def __str__(self):
        return "{0}, {1}, {2}, {3}".format(self.left, self.top, self.width,
                                           self.height)


#----------------------------------------------------------
cdef class FloatRect(object):
    """
    Utility class for manipulating 2D axis aligned rectangles.

    A rectangle is defined by its top-left corner and its size.

    It is a very simple class defined for convenience, so its member variables
     (left, top, width and height) are public and can be accessed directly,
     just like the vector classes (Vector2 and Vector3).

    To keep things simple, sf::Rect doesn't define functions to emulate the
    properties that are not directly members (such as right, bottom, center,
    etc.), it rather only provides intersection functions.

    sf::Rect uses the usual rules for its boundaries:

    The left and top edges are included in the rectangle's area
    The right (left + width) and bottom (top + height) edges are excluded from
    the rectangle's area
    This means that sf::IntRect(0, 0, 1, 1) and sf::IntRect(1, 1, 1, 1)
    don't intersect.

    sf::Rect is a template and may be used with any numeric type, but for
    simplicity the instanciations used by SFML are typedefed:

    sf::Rect<float> is sf::FloatRect -> gterm.FloatRect
    """
    cdef sfFloatRect m_rect

    def __init__(self, left=0.0, top=0.0, width=0.0, height=0.0):
        self.m_rect.left = left
        self.m_rect.top = top
        self.m_rect.width = width
        self.m_rect.height = height

    def contains(self, point):
        """
        Checks if the rect contains a point
        """
        return self.m_rect.contains(point[0], point[1])

    def contains(self, FloatRect rect):
        """
        Checks if the rect contains a point
        """
        return self.m_rect.intersects(rect.m_rect)

    property left:
        """
        The left coordinate (x)
        """
        def __set__(self, value):
            self.m_rect.left = value

        def __get__(self):
            return self.m_rect.left

    property top:
        """
        The top coordinate (y)
        """
        def __set__(self, value):
            self.m_rect.top = value

        def __get__(self):
            return self.m_rect.top

    property width:
        """
        The width of the rectangle
        """
        def __set__(self, value):
            self.m_rect.width = value

        def __get__(self):
            return self.m_rect.width

    property height:
        """
        The height of the rectangle
        """
        def __set__(self, value):
            self.m_rect.height = value

        def __get__(self):
            return self.m_rect.height


#----------------------------------------------------------
cdef class Time(object):
    """
    Represents a time value
    """
    cdef sfTime m_time

    def __cinit__(self, *args, **kargs):
        pass

    def as_seconds(self):
        """
        Returns the time value as a number of seconds

        :return: Number of seconds
        :rtype: float
        """
        return self.m_time.asSeconds()

    def as_milliseconds(self):
        """
        Returns the time value as a number of milliseconds

        :return: Number of milliseconds
        :rtype: int
        """
        return self.m_time.asMilliseconds()

    def as_microseconds(self):
        """
        Returns the time value as a number of microseconds

        :return: Number of microseconds
        :rtype: int
        """
        return self.m_time.asMicroseconds()

    @classmethod
    def from_seconds(cls, amount):
        """
        Constructs a sf::Time value from a number of seconds

        :param amount; Number of seconds
        :type amount; float

        :return gterm.Time
        """
        t = Time()
        t.m_time = sfSeconds(amount)
        return t

    @classmethod
    def from_milliseconds(cls, amount):
        """
        Constructs a sf::Time value from a number of milliseconds

        :param amount; Number of milliseconds
        :type amout: int

        :return gterm.Time
        """
        t = Time()
        t.m_time = sfMilliseconds(amount)
        return t

    @classmethod
    def from_microseconds(cls, amount):
        """
        Constructs a sf::Time value from a number of microseconds

        :param amount; Number of microseconds
        :type amount: int

        :return gterm.Time
        """
        t = Time()
        t.m_time = sfMicroSeconds(amount)
        return t


#----------------------------------------------------------
cdef class Clock(object):
    """
    Utility class that measures the elapsed time
    """
    cdef sfClock ck

    def __init__(self):
        self.ck.restart()

    property elapsed_time:
        """
        Gets the elapsed time.

        This function property returns the time elapsed since the last call
        to restart() (or the construction of the instance if restart()
        has not been called).
        """
        def __get__(self):
            t = Time()
            t.m_time = self.ck.getElapsedTime()
            return t

    def restart(self):
        """ Restarts the clock

        This function puts the time counter back to zero.
        It also returns the time elapsed since the clock was started.

        :return Time elapsed
        :rtype: pyGTerm.gterm.Time
        """
        t = Time()
        t.m_time = self.ck.restart()
        return t


cdef class Sound(object):
    """
    Wraps the sf::Sound class.

    .. warning:: Never create a sound instance yourself (the internal sf::Sound
                 is set to null), always use GameItem.addSound
    """
    cdef sfSound* thisptr

    def __cinit__(self, *args, **kargs):
        self.thisptr = NULL

    def play(self):
        """
        Plays the sound
        """
        if self.thisptr:
            self.thisptr.play()

    def pause(self):
        """
        Pause the sound
        """
        if self.thisptr:
            self.thisptr.pause()

    def stop(self):
        """
        Stops the sound
        """
        if self.thisptr:
            self.thisptr.stop()

    property status:
        """
        Gets the sound status
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.getStatus()
            return None

    property playing_offset:
        """
        Gets/sets the sound playing offset
        """
        def __set__(self, Time value):
            if self.thisptr:
                self.thisptr.setPlayingOffset(value.m_time)

        def __get__(self):
            cdef Time t = Time()
            if self.thisptr:
                t.m_time = self.thisptr.getPlayingOffset()
                return t
            return None

    property loop:
        """
        Gets/Sets the loop flag
        """
        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setLoop(value)

        def __get__(self):
            if self.thisptr:
                return self.thisptr.getLoop()
            return False

    property pitch:
        """
        Gets/sets the pitch of the sound
        """
        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setPitch(value)

        def __get__(self):
            if self.thisptr:
                return self.thisptr.getPitch()
            return None

    property volume:
        """
        Gets/Sets the sound's volume
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.getVolume()
            return None

        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setVolume(value)

    property position:
        """
        Gets/Sets the sound position (relative to a sound listener)
        """
        def __set__(self, position):
            if self.thisptr:
                self.thisptr.setPosition(position[0], position[1], position[2])

        def __get__(self):
            cdef Vector3f pos
            if self.thisptr:
                pos = self.thisptr.getPosition()
                return pos.x, pos.y, pos.z

    property relative_to_listener:
        """
        Gets/sets the relativeToListener flag
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.isRelativeToListener()
            return None

        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setRelativeToListener(value)

    property min_distance:
        """
        Gets/Sets the sound min distance
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.getMinDistance()
            return None

        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setMinDistance(value)

    property attenuation:
        """
        Gets/sets the sound attenuation
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.getAttenuation()
            return None

        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setAttenuation(value)



cdef class Music(object):
    """
    Wraps the sf::Music class.

    .. warning:: Never create a music instance yourself (the internal sf::Music
                 is set to null), always use GameItem.addMusic.
    """
    cdef sfMusic* thisptr

    def __cinit__(self, *args, **kargs):
        self.thisptr = NULL

    property duration:
        """
        Gets the music's duration
        """
        def __get__(self):
            cdef Time t = Time()
            if self.thisptr:
                t.m_time = self.thisptr.getDuration()
                return t
            return None

    property channel_count:
        """
        Gets the number of channel (2 means stereo)
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.getChannelCount()
            return None

    property sample_rate:
        """
        Gets the sample rate
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.getSampleRate()
            return None

    def play(self):
        """
        Plays the music
        """
        if self.thisptr:
            self.thisptr.play()

    def pause(self):
        """
        Pauses the music
        """
        if self.thisptr:
            self.thisptr.pause()

    def stop(self):
        """
        Stops the music
        """
        if self.thisptr:
            self.thisptr.stop()

    property status:
        """
        Gets the playing status
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.getStatus()
            return None

    property playing_offset:
        """
        Gets the playing offset
        """
        def __set__(self, Time value):
            if self.thisptr:
                self.thisptr.setPlayingOffset(value.m_time)

        def __get__(self):
            cdef Time t = Time()
            if self.thisptr:
                t.m_time = self.thisptr.getPlayingOffset()
                return t
            return None

    property loop:
        """
        Gets/Sets the loop flag
        """
        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setLoop(value)

        def __get__(self):
            if self.thisptr:
                return self.thisptr.getLoop()
            return False

    property pitch:
        """
        Gets/Sets the pitch of the music
        """
        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setPitch(value)

        def __get__(self):
            if self.thisptr:
                return self.thisptr.getPitch()
            return None

    property volume:
        """
        Gets/Sets the music's volume
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.getVolume()
            return None

        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setVolume(value)

    property position:
        """
        Gets/sets the music position
        """
        def __set__(self, position):
            if self.thisptr:
                self.thisptr.setPosition(position[0], position[1], position[2])

        def __get__(self):
            cdef Vector3f pos
            if self.thisptr:
                pos = self.thisptr.getPosition()
                return pos.x, pos.y, pos.z

    property relative_to_listener:
        """
        Gets/Sets the relative to listener flag value
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.isRelativeToListener()
            return None

        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setRelativeToListener(value)

    property min_distance:
        """
        Gets/Sets the min distance
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.getMinDistance()
            return None

        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setMinDistance(value)

    property attenuation:
        """
        Gets/Sets the music attenuation
        """
        def __get__(self):
            if self.thisptr:
                return self.thisptr.getAttenuation()
            return None

        def __set__(self, value):
            if self.thisptr:
                self.thisptr.setAttenuation(value)


#----------------------------------------------------------
cdef class Color(object):
    """
    Represents a color value
    """
    #: Predefined color: BLACK
    BLACK = Color(0, 0, 0)
    #: Predefined color: WHITE
    WHITE = Color(255, 255, 255)
    #: Predefined color: RED
    RED = Color(255, 0, 0)
    #: Predefined color: GREEN
    GREEN = Color(0, 255, 0)
    #: Predefined color: BLUE
    BLUE = Color(0, 0, 255)
    #: Predefined color: YELLOW
    YELLOW = Color(255, 255, 0)
    #: Predefined color: MAGENTA
    MAGENTA = Color(255, 0, 255)
    #: Predefined color: CYAN
    CYAN = Color(0, 255, 255)
    #: Predefined color: TRANSPARENT
    TRANSPARENT = Color(0, 0, 0, 0)

    cdef sfColor m_color

    def __init__(self, r=255, g=255, b=255, a=255):
        """
        Creates the color instance

        :param r: Red channel (0-255)
        :type r: int

        :param g: Green channel (0-255)
        :type g: int

        :param b: Blue channel (0-255)
        :type b: int

        :param a: Alpha channel (0-255)
        :type a: int
        """
        self.m_color.r = r
        self.m_color.g = g
        self.m_color.b = b
        self.m_color.a = a

    property r:
        """
        The RED component of the color (byte)
        """
        def __get__(self):
            return self.m_color.r

        def __set__(self, r):
            self.m_color.r = r

    property g:
        """
        The GREEN component of the color (byte)
        """
        def __get__(self):
            return self.m_color.g

        def __set__(self, g):
            self.m_color.g = g

    property b:
        """
        The BLUE component of the color (byte)
        """
        def __get__(self):
            return self.m_color.b

        def __set__(self, b):
            self.m_color.b = b

    property a:
        """
        The ALPHA component of the color (byte)
        """
        def __get__(self):
            return self.m_color.a

        def __set__(self, unsigned int a):
            self.m_color.a = a

def get_bit_value(byteval, idx):
    """
    Returns a bit value contained in the byteval at the specified index.

    :param byteval: The byte (word,long) value from which a single bit value
     must be extracted

    :param idx: index of the bit insided the byte

    :rtype: bool

    :return: A boolean representing the bit value
    """
    return (byteval & (1 << idx)) != 0


def error(msg):
    """ Logs an error message """
    Error(msg.encode("latin-1"))

def warning(msg):
    """ Logs a warning message """
    Warning(msg.encode("latin-1"))

def info(msg):
    """ Logs an info message """
    Info(msg.encode("latin-1"))


cdef class Score(object):
    """
    The Score class is an utility class to help manipulate score.

    A score is a 4 bytes wide value. The MSB is used as a bitmask for
    formatting.
    """
    #: c++ instance
    cdef cScore* thisptr

    def __cinit__(self, value):
        """
        Allocates the gt::Score

        :param value: The score value (Uint32)
        """
        self.thisptr = new cScore(value)

    def __dealloc__(self):
        """
        Delete c++ instance
        """
        del self.thisptr

    property value:
        """
        Gets/Sets the score value
        """
        def __get__(self):
            return self.thisptr.getValue()

        def __set__(self, value):
            self.thisptr.setValue(value)

    def to_string(self, nb_digits, nb_decimal_digits):
        """
        Return the score as a string
        """
        return self.thisptr.toString(nb_digits, nb_decimal_digits)

    property blink:
        """
        Checks if the score must blink
        """
        def __get__(self):
            return self.thisptr.mustBlink()

    property transparent:
        """
        Checks if the score is transparent
        """
        def __get__(self):
            return self.thisptr.isTransparent()
