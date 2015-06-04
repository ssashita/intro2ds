// testmap.js by Michael Geary
// Use under the Unlicense or the MIT License: see LICENSE for details

// Outer wrapper function
(function( $ ) {

var states = PolyMap.states;
var polyTimer;

function S() {
	return Array.prototype.join.call( arguments, '' );
}

function htmlEscape( str ) {
	var div = document.createElement( 'div' );
	div.appendChild( document.createTextNode( str ) );
	return div.innerHTML;
}

function optionHTML( value, name, selected, disabled ) {
	var id = value ? 'id="option-' + value + '" ' : '';
	var style = disabled ? 'color:#AAA; font-style:italic; font-weight:bold;' : '';
	selected = selected ? 'selected="selected" ' : '';
	disabled = disabled ? 'disabled="disabled" ' : '';
	return S(
		'<option ', id, 'value="', value, '" style="', style, '" ', selected, disabled, '>',
			name,
		'</option>'
	);
}

function randomInt( n ) {
	return Math.floor( Math.random() * n );
}

function randomElement( array ) {
	return array[ randomInt(array.length) ];
};

(function() {
	var index = 0;
	function option( value, name, selected, disabled ) {
		var html = optionHTML( value, name, selected, disabled );
		++index;
		return html;
	}
	function stateOption( state, selected ) {
		state.selectorIndex = index;
		return option( state.abbr, state.name, selected );
	}
	
	stateSelector = function() {
		return S(
			'<select id="stateSelector">',
				option( 'US', '50 States, DC, and Puerto Rico', true ),
				option( 'CONGRESSIONAL', 'All US Congressional Districts' ),
				option( 'COUNTY', 'All 3199 Counties (slow in IE!)' ),
				states.map( function( state ) {
					return stateOption( state, false );
				}).join(''),
			'</select>'
		);
	}
})();

function load() {
	var state, region, marker;
	var $window = $(window), $testmap = $('#testmap');
	
	resize = function() {
		var left = $('#panel').width();
		$testmap.css({
			left: left + 1,
			top: 0,
			width: $window.width() - left - 2,
			height: $window.height()
		})
		
		pm && pm.resize();
	};
	
	$window.resize( resize );
	resize();
	
	var pm = window.pm = new PolyMap({
		container: $testmap[0],
		shapes: '../shapes/json/',
		events: {
			load: function( region_ ) {
				region = region_;
				colorize( region );
			},
			drew: function() {
				if( $('#chkAnimate').attr('checked') ) {
					clearTimeout( polyTimer );
					polyTimer = setTimeout( function() {
						log.reset( true );
						colorize( region );
						pm.redraw();
					}, 25 );
				}
			},
			over: function( feature ) {
				$('#status').html( featureName(feature) );
				if( marker ) {
					pm.removeMarker( marker );
					marker = null;
				}
				if( feature ) {
					var centroid = feature.properties.centroid;
					var latlng = new google.maps.LatLng( centroid[1], centroid[0] );
					marker = new google.maps.Marker( pm.v2 ? latlng : { position: latlng } );
					pm.addMarker( marker );
				}
			},
			click: function( feature ) {
				alert( 'Clicked ' + featureName(feature) );
			}
		}
	});
	
	$('#chkAnimate').click( function() {
		if( this.checked ) {
			pm.redraw();
		}
		else {
			clearTimeout( polyTimer );
			polyTimer = null;
		}
	});
	
	//$('#chkSubpixel').click( function() {
	//	pm.redraw();
	//});
	
	$('#chkMarkers').click( function() {
		if( region && region.geo ) region.geo.markers = !! this.checked;
		pm && pm.redraw();
	});
	
	var match = location.search.match( /\Wstate=(\w+)/ );
	var abbr = match && match[1] || 'US';
	$('#stateSelector')
		.val( abbr.toUpperCase() )
		.change( stateSelectorChange )
		.keyup( stateSelectorChange )
		.trigger( 'change' );
	
	function testMarker( name ) {
		return {
			url: 'images/' + name + '.png',
			size: { x: 16, y: 16 },
			anchor: { x: 7, y: 7 }
		};
	}
	var testMarkers = [ testMarker('add'), testMarker('delete') ];
	
	function colorize( region ) {
		// Test with random colors
		region.geo.markers = !! $('#chkMarkers')[0].checked;
		( region.geo.features || [region] ).forEach( function( feature ) {
			//feature.fillColor = '#FFFFFF';
			//feature.fillOpacity = 0;
			feature.fillColor = '#' + Math.random().toString(16).slice(2,8);
			feature.fillOpacity = Math.random() * .5 + .1;
			feature.strokeColor = '#000000';
			feature.strokeOpacity = 0.2;
			feature.strokeWidth = 1.5;
			feature.marker = randomElement( testMarkers );
		});
	}
	
	function featureName( feature ) {
		if( ! feature ) return 'nowhere';
		var props = feature.properties;
		var abbr = props.state || feature.container.properties.state;
		var state = PolyMap.stateByAbbr(abbr).name;
		var local = feature.properties.name;
		switch( props.kind ) {
			case 'cd': return state + ( local == 'One' ? ' (one district)' : ' District ' + local );
			case 'county': return local + ' County, ' + state;
		}
		return state;
	}
	
	function stateSelectorChange() {
		loadState( this.value.replace('!','').toLowerCase() );
	}
	
	function loadState( value ) {
		if( value == state ) return;
		state = value;
		pm.load({ region:state });
	}
}

$(window).bind( 'load', load );

})( jQuery );
// end outer wrapper function
