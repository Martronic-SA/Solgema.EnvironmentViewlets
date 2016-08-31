from zope import interface, component
import interfaces
import options
      

#################################
# Real Estate Content

BandeauContentStorage = options.PersistentOptions.wire( "BandeauContentStorage", "Solgema.EnvironmentViewlets.bandeau", interfaces.IBandeauContent )

class BandeauContentAdapter( BandeauContentStorage ):

    interface.implements( interfaces.IBandeauContent )
    
    def __init__( self, context ):
        self.context = context

FooterContentStorage = options.PersistentOptions.wire( "FooterContentStorage", "Solgema.EnvironmentViewlets.footer", interfaces.IFooterContent )

class FooterContentAdapter( FooterContentStorage ):

    interface.implements( interfaces.IFooterContent )
    
    def __init__( self, context ):
        self.context = context

PrintFooterContentStorage = options.PersistentOptions.wire( "PrintFooterContentStorage", "Solgema.EnvironmentViewlets.printfooter", interfaces.IPrintFooterContent )

class PrintFooterContentAdapter( PrintFooterContentStorage ):

    interface.implements( interfaces.IPrintFooterContent )
    
    def __init__( self, context ):
        self.context = context

LogoContentStorage = options.PersistentOptions.wire( "LogoContentStorage", "Solgema.EnvironmentViewlets.logo", interfaces.ILogoContent )

class LogoContentAdapter( LogoContentStorage ):

    interface.implements( interfaces.ILogoContent )
    
    def __init__( self, context ):
        self.context = context

PrintLogoContentStorage = options.PersistentOptions.wire( "PrintLogoContentStorage", "Solgema.EnvironmentViewlets.printlogo", interfaces.IPrintLogoContent )

class PrintLogoContentAdapter( PrintLogoContentStorage ):

    interface.implements( interfaces.IPrintLogoContent )
    
    def __init__( self, context ):
        self.context = context

BackgroundContentStorage = options.PersistentOptions.wire( "BackgroundContentStorage", "Solgema.EnvironmentViewlets.background", interfaces.IBackgroundContent )

class BackgroundContentAdapter( BackgroundContentStorage ):

    interface.implements( interfaces.IBackgroundContent )
    
    def __init__( self, context ):
        self.context = context

