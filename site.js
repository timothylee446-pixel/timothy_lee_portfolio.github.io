// Shows a labeled placeholder when an image or video file has not been added yet.
function placeholder(el){
  var d=document.createElement('div');
  d.className='missing';
  d.textContent='Add file: '+el.dataset.name;
  el.replaceWith(d);
}
document.querySelectorAll('img[data-name]').forEach(function(img){
  img.addEventListener('error',function(){placeholder(img)});
  if(img.complete && img.naturalWidth===0) placeholder(img);
});
document.querySelectorAll('video[data-name]').forEach(function(v){
  v.addEventListener('error',function(){placeholder(v)});
});
