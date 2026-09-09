# ******************************************************************************
#  Not copyrighted. Free for usage without warranty, expressed or implied
#
#  Method of static initialzation commonly found on search of World Wide Web
#
#  Filename   : static_init.py
#  Description:
#    Defines the static_init decorator for Python classes. The method of static
#    initialization of Python classes is commonly found on a search of the
#    internet
#
#    Decorate the class definition with the @static_init decorator
#    Within the class, define a @classmethod named static_init(cls)
#    Define class static variables and constants within the static_int() method
#
#    Example:
#    @static_init
#    class foobar:
#        @classmethod
#        def static_init(cls):
#            cls.__DEEP_THOUGHT = 42
#            cls.__connected_devices = 0
#
#  Change log:
#    2025-09-20  KSM  Created
#    2026-09-09  KSM  Updated the comment to include this change log
#
#  Author     : Kerry S. Martin, wssm243@gmail.com
# ******************************************************************************

def static_init(cls):
    """static initialization class decorator
    """
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls


# ******************************************************************************
#  Implementation by Kerry S. Martin, wssm243@gmail.com
#  Not copyrighted. Free for usage without warranty, expressed or implied
# ******************************************************************************