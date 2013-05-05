# coding: utf-8
import os
import sys
import time
import traceback
import subprocess

from optparse import make_option

from django.core.management.base import BaseCommand


from dext.utils import pid


def construct_command(environment, worker):

    class Command(BaseCommand):

        help = 'run "%s"' % worker.name

        requires_model_validation = False

        @pid.protector(worker.pid)
        def handle(self, *args, **options):

            try:
                environment.clean_queues()
                worker.initialize()
                worker.run()
            except KeyboardInterrupt:
                pass
            except Exception:
                traceback.print_exc()
                worker.logger.error('Infrastructure worker exception: %s' % worker.name,
                                    exc_info=sys.exc_info(),
                                    extra={} )


            environment.deinitialize()

    return Command


def construct_workers_manager(help, pid, workers):

    workers = filter(lambda worker: worker is not None, workers)

    class Command(BaseCommand):

        help = help

        requires_model_validation = False

        option_list = BaseCommand.option_list + ( make_option('-c', '--command',
                                                              action='store',
                                                              type=str,
                                                              dest='command',
                                                              help='start|stop|restart|status'), )

        def start(self):
            for worker in workers:
                with open(os.devnull, 'w') as devnull:
                    subprocess.Popen(['./manage.py', worker.command_name], stdin=devnull, stdout=devnull, stderr=devnull)


        def stop(self):
            for worker in reversed(workers):
                if worker.stop_signal_required and pid.check(worker.pid):
                    print '%s found, send stop command' % worker.name
                    worker.cmd_stop()
                    print 'waiting answer'
                    answer_cmd = worker.stop_queue.get(block=True)
                    answer_cmd.ack()
                    print 'answer received'

            while any(pid.check(worker.pid) for worker in workers):
                time.sleep(0.1)


        def force_stop(self):
            for worker in reversed(workers):
                pid.force_kill(worker.command_name)


        @pid.protector(pid)
        def handle(self, *args, **options):
            command = options['command']

            if command == 'start':
                self.start()
                print 'infrastructure start'

            elif command == 'stop':
                self.stop()
                print 'infrastructure stopped'

            elif command == 'force_stop':
                self.force_stop()
                print 'infrastructure stopped (force)'

            elif command == 'restart':
                self.start()
                self.stop()
                print 'infrastructure restarted'

            elif command == 'status':
                print 'command "%s" does not implemented yet ' % command

            else:
                print 'command did not specified'