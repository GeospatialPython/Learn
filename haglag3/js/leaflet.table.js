

L.control.Table = L.Control.extend({

  options: {
      position: 'bottomleft',
      handler: {}
  },

  containers:{},

  addTable: function(table,rel,title) {

    this.containers[rel] = table;
    table.style.display='none';

    this.tables.appendChild(table);

    var option = L.DomUtil.create('option');
    option.value=rel;
    option.innerHTML=title;
    this.switcher.appendChild(option);

    return table;
  },

  onAdd: function(map) {
    this._map=map;

    L.DomEvent.addListener(this.control, 'mouseover',function(){
      map.dragging.disable();
      map.doubleClickZoom.disable();
      map.scrollWheelZoom.disable();
    },this);

    L.DomEvent.addListener(this.control, 'mouseout',function(){
      map.dragging.enable();
      map.doubleClickZoom.enable();
      map.scrollWheelZoom.enable();
    },this);

    return this.control;
  },

  initialize: function(){
    var that = this;

    var control = L.DomUtil.create('div','leaflet-control leaflet-table-container');
    var inner = L.DomUtil.create('div');

    var tables = L.DomUtil.create('div','leaflet-tables-container');
    this.tables = tables;

    var switcher = L.DomUtil.create('select','leaflet-table-select');
    switcher.addEventListener('change',function(evt){
        var curr = evt.target[evt.target.selectedIndex].value;
        for(var rel in that.containers) {
          var container = that.containers[rel];
          if(rel==curr && container.style.display != 'block') {
            container.style.display='block';
          } else {
            container.style.display='none';
          }
        }
    },false);
    this.switcher=switcher;

    var option = L.DomUtil.create('option');
    option.value='none';
    option.innerHTML='Tables';
    switcher.appendChild(option);

    control.appendChild(inner);
    inner.appendChild(switcher);
    inner.appendChild(tables);

    control.onmousedown = control.ondblclick = L.DomEvent.stopPropagation;

    this.control=control;
  }
});

