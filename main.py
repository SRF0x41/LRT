from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from Navigation import Navigation


class LRT(App):
    def build(self):
        # Create label to display coordinates
        self.label = Label(
            text='Waiting for GPS...',
            size_hint=(.5, .5),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        

        # Create Navigation object and link it to the label
        self.nav_object = Navigation(self.update_label)
        self.nav_object.start()

        return self.label

    def update_label(self, coords_text):
        """Called whenever GPS coordinates are updated."""
        # Ensure updates happen on the main UI thread
        setattr(self.label, 'text', coords_text)

        
if __name__ == '__main__':
    app = LRT()
    app.run()
        
        