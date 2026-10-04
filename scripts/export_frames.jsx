// Copy and configure this script. Run only after export is requested.
(function(){
 var COMP_NAME='YOUR_ALPHA_COMPOSITION';
 var OUTPUT_DIR='C:/your-project/output/frames';
 var c=null;for(var j=1;j<=app.project.numItems;j++){var item=app.project.item(j);if(item instanceof CompItem&&item.name===COMP_NAME)c=item;}
 if(!c)throw new Error('Target composition not found: '+COMP_NAME);
 var folder=new Folder(OUTPUT_DIR);if(folder.exists)throw new Error('Choose a new output directory; existing frames will not be overwritten');
 if(!folder.create())throw new Error('Cannot create frame directory');
 var count=Math.round(c.duration*c.frameRate);
 for(var i=0;i<count;i++)c.saveFrameToPng(i/c.frameRate,new File(folder.fsName+'/frame_'+('000000'+i).slice(-6)+'.png'));
 var marker=new File(folder.fsName+'/complete.json');marker.open('w');marker.write('{"frames":'+count+',"fps":'+c.frameRate+',"width":'+c.width+',"height":'+c.height+'}');marker.close();
})();
