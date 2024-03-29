var Service = require('node-windows').Service;

// Create a new service object
var svc = new Service({
  name:'cm-logs-vue',
  description: 'Frontend for cm logs screen',
  script: '.\\server.js',
  nodeOptions: [
    '--harmony',
    '--max_old_space_size=4096'
  ]
  //, workingDirectory: '...'
  //, allowServiceLogon: true
});

// Listen for the "install" event, which indicates the
// process is available as a service.
svc.on('install',function(){
  svc.start();
});

svc.install();