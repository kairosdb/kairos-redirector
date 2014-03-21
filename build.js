var rules = Packages.tablesaw.rules;
var tablesaw = Packages.tablesaw;
var redline = Packages.org.freecompany.redline;

saw.setProperty(saw.PROP_MULTI_THREAD_OUTPUT, 'on');

var project = 'kairos-redirector';
var version = '1.0.0';
var release = '1'; //package release number
var installBase = '/opt/'+project;
var buildDir = 'build';
var rpmFile = project + '-' + version + '-' + release + '.rpm';
var srcRpmFile = project + '-' + version + '-' + release + '.src.rpm';

var buildDirRule = new rules.DirectoryRule("build");

var rpmRule = new rules.SimpleRule('build-rpm')
		.addTarget(buildDir+'/'+rpmFile)
		.setMakeAction('doRPM')
		.addDepend(buildDirRule)
		.alwaysRun();
	
function addFileSetToRPM(builder, destination, fileSet)
{
	var paths = fileSet.getFiles();
	
	for (var i = 0; i < paths.size(); i++)
	{
		var path = paths.get(i); 
		//print('Adding '+path);
		var f = new java.io.File(path.getBaseDir(), path.getFile());
		builder.addFile(destination + "/" + path.getFile(), f)
	}
}
	
function doRPM(rule)
{
	var host = java.net.InetAddress.getLocalHost().getHostName();
	
	var rpmBuilder = new redline.Builder();
	rpmBuilder.setDescription('description goes here');
	rpmBuilder.setGroup('Applications/Internet');
	rpmBuilder.setLicense('license');
	rpmBuilder.setPackage(project, version, release);
	rpmBuilder.setPlatform(redline.header.Architecture.NOARCH, redline.header.Os.LINUX);
	rpmBuilder.setSummary('summary');
	rpmBuilder.setType(redline.header.RpmType.BINARY);
	rpmBuilder.setUrl('http://proofpoint.com');
	rpmBuilder.setVendor('Proofpoint Inc.');
	rpmBuilder.setProvides(project);
	rpmBuilder.setBuildHost(host);
	rpmBuilder.setSourceRpm(srcRpmFile);
	
	//Adding dependencies
	//rpmBuilder.addDependencyMore('httpd', '2');
	
	addFileSetToRPM(rpmBuilder, installBase+'/app', new tablesaw.RegExFileSet('app', '.*').recurse());
	addFileSetToRPM(rpmBuilder, installBase+'/lib', new tablesaw.RegExFileSet('lib', '.*').recurse());
	addFileSetToRPM(rpmBuilder, installBase+'/plugins', new tablesaw.RegExFileSet('plugins', '.*').recurse());
	
	rpmBuilder.addFile(installBase+'/index.php', new java.io.File('index.php'));
	rpmBuilder.addFile(installBase+'/.htaccess', new java.io.File('.htaccess'));
	rpmBuilder.addFile('/etc/httpd/conf.d/jslate.conf', new java.io.File('etc/jslate.conf'));

	//Post install script to set owner to apache
	rpmBuilder.setPostInstallScript(new java.io.File("etc/post_install.sh"));
	//rpmBuilder.setPreUninstallScript(new File("src/scripts/install/pre_uninstall.sh"));
	
	print("Building RPM "+rule.getTarget())
	var outputFile = new java.io.FileOutputStream(rule.getTarget())
	rpmBuilder.build(outputFile.getChannel())
	outputFile.close()
}

new rules.SimpleRule('run').setDescription('Start the python application')
		.setMakeAction('doRun')
		.alwaysRun();
		
function doRun(rule)
{
	saw.setProperty('PYTHONPATH', 'src/main/python');
	var cmd = 'python src/main/python/start.py';
	localIni = new java.io.File("redirector.ini");
	if (localIni.exists())
		cmd += ' redirector.ini';
	else
		cmd += ' src/main/resource/redirector.ini';
	
	saw.exec(cmd);
}

new rules.SimpleRule('test').setDescription("Run PyUnit tests")
		.setMakeAction('doTest')
		.alwaysRun();
		
function doTest(rule)
{
	saw.setProperty('PYTHONPATH', 'src/main/python');
	print("running this");
	var testFiles = new tablesaw.RegExFileSet('src/test/python', '.*\\.py').getFullFilePaths();
	for (i = 0; i < testFiles.size(); i++)
	{
		print(testFiles.get(i));
		saw.exec('python '+testFiles.get(i));
	}
}

saw.setDefaultTarget('build-rpm');
