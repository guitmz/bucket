from cmd import Cmd

class BucketPrompt(Cmd):

    def do_use(self, args):
        """Changes your current bucket."""
        if len(args) == 0:
            print("I need a bucket name!")
        else:
            try:
                self.bucket_name = args
                print("Using bucket %s" % self.bucket_name)
            except:
                print("Invalid bucket!")

    def do_pwd(self, args):
        """Shows which bucket you are using."""
        try:
            print('You are using the following bucket: %s' % self.bucket_name)
        except AttributeError:
            print("Undefined bucket!")
    
    def do_up(self, args):
        """Uploads a file to your current bucket."""

    
    def do_ls(self, args):
        """List files and folders in your current bucket."""
    
    
    def do_quit(self, args):
        """Quits the program."""
        print("¯\_(ツ)_/¯")
        raise SystemExit


if __name__ == '__main__':
    prompt = BucketPrompt()
    prompt.prompt = '>_ '
    prompt.cmdloop('Starting prompt...')
