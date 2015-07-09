// Adapted from nvd3.org Line With View Finder
// http://nvd3.org/examples/lineWithFocus.html
// and multichart http://nvd3.org/examples/linePlusBar.html

twoAxisFocusChart = function() {
    "use strict";

    //============================================================
    // Public Variables with Default Settings
    //------------------------------------------------------------

    var yScale1 = d3.scale.linear()
        , yScale2 = d3.scale.linear()
        , yScaleC = d3.scale.linear()
        , lines1 = nv.models.line().yScale(yScale1)
        , lines2 = nv.models.line().yScale(yScale2)
        , linesC = nv.models.line().yScale(yScaleC)
        , xAxis = nv.models.axis().orient('bottom').tickPadding(5)
        , y1Axis = nv.models.axis().scale(yScale1).orient('left')
        , y2Axis = nv.models.axis().scale(yScale2).orient('right')
        , xCAxis = nv.models.axis().orient('bottom').tickPadding(5)
        , yCAxis = nv.models.axis().scale(yScaleC).orient('left')
        , legend = nv.models.legend()
        , brush = d3.svg.brush()

        ;

    var margin = {top: 30, right: 30, bottom: 30, left: 60}
        , margin2 = {top: 10, right: 30, bottom: 20, left: 60}
        , color = nv.utils.defaultColor()
        , width = null
        , height = null
        , height2 = 100
        , x
        , y1
        , y2
        , xC
        , yC
        , showLegend = true
        , brushExtent = null
        , tooltips = true
        , tooltip = function(key, x, y, e, graph) {
            return '<h3>' + key + '</h3>' +
                '<p>' +  y + ' at ' + x + '</p>'
        }
        , noData = "No Data Available."
        , dispatch = d3.dispatch('tooltipShow', 'tooltipHide', 'brush', 'stateChange', 'changeState')
        , transitionDuration = 250
        , state = nv.utils.state()
        , defaultState = null
        , yDomain1
        , yDomain2
        , yDomainC
        , getX = function(d) {return d.x }
        , getY = function(d) {return d.y }
        , interpolate = 'monotone'
        ;

    lines1.clipEdge(true);
    lines2.clipEdge(true);
    linesC.interactive(false).clipEdge(true);

    //============================================================
    // Private Variables
    //------------------------------------------------------------

    var showTooltip = function(e, offsetElement) {
        var left = e.pos[0] + ( offsetElement.offsetLeft || 0 ),
            top = e.pos[1] + ( offsetElement.offsetTop || 0),
            x = xAxis.tickFormat()(lines1.x()(e.point, e.pointIndex)),
            y = y1Axis.tickFormat()(lines1.y()(e.point, e.pointIndex)),
            content = tooltip(e.series.key, x, y, e, chart);

        nv.tooltip.show([left, top], content, null, null, offsetElement);
    };

    var stateGetter = function(data) {
        return function(){
            return {
                active: data.map(function(d) { return !d.disabled })
            };
        }
    };

    var stateSetter = function(data) {
        return function(state) {
            if (state.active !== undefined)
                data.forEach(function(series,i) {
                    series.disabled = !state.active[i];
                });
        }
    };

    function chart(selection) {
        selection.each(function(data) {
            var container = d3.select(this),
                that = this;
            nv.utils.initSVG(container);
            var availableWidth = (width  || parseInt(container.style('width')) || 960)
                    - margin.left - margin.right,
                availableHeight1 = (height || parseInt(container.style('height')) || 400)
                    - margin.top - margin.bottom - height2,
                availableHeight2 = height2 - margin2.top - margin2.bottom;

            var dataLines1 = data.filter(function(d) {return d.yAxis == 1});
            var dataLines2 = data.filter(function(d) {return d.yAxis == 2});

            chart.update = function() { container.transition().duration(transitionDuration).call(chart) };
            chart.container = this;

            state
                .setter(stateSetter(data), chart.update)
                .getter(stateGetter(data))
                .update();

            // DEPRECATED set state.disableddisabled
            state.disabled = data.map(function(d) { return !!d.disabled });

            if (!defaultState) {
                var key;
                defaultState = {};
                for (key in state) {
                    if (state[key] instanceof Array)
                        defaultState[key] = state[key].slice(0);
                    else
                        defaultState[key] = state[key];
                }
            }

            // Display No Data message if there's nothing to show.
            if (!data || !data.length || !data.filter(function(d) { return d.values.length }).length) {
                var noDataText = container.selectAll('.nv-noData').data([noData]);

                noDataText.enter().append('text')
                    .attr('class', 'nvd3 nv-noData')
                    .attr('dy', '-.7em')
                    .style('text-anchor', 'middle');

                noDataText
                    .attr('x', margin.left + availableWidth / 2)
                    .attr('y', margin.top + availableHeight1 / 2)
                    .text(function(d) { return d });

                return chart;
            } else {
                container.selectAll('.nv-noData').remove();
            }

            var series1 = data.filter(function(d) {return !d.disabled && d.yAxis == 1})
                .map(function(d) {
                    return d.values.map(function(d,i) {
                        return { x: d.x, y: d.y }
                    })
                });

            var series2 = data.filter(function(d) {return !d.disabled && d.yAxis == 2})
                .map(function(d) {
                    return d.values.map(function(d,i) {
                        return { x: d.x, y: d.y }
                    })
                });

            // Setup Scales
            x = lines1.xScale();
            y1 = lines1.yScale();
            y2 = lines2.yScale();
            xC = linesC.xScale();
            yC = linesC.yScale();

            // x.domain(d3.extent(d3.merge(series1.concat(series2)), function(d) { return d.x } ))
            //     .range([0, availableWidth]);

            // Setup containers and skeleton of chart
            var wrap = container.selectAll('g.nv-wrap.nv-twoAxisFocusChart').data([data]);
            var gEnter = wrap.enter().append('g').attr('class', 'nvd3 nv-wrap nv-twoAxisFocusChart').append('g');
            var g = wrap.select('g');
            gEnter.append('g').attr('class', 'legendWrap');

            var focusEnter = gEnter.append('g').attr('class', 'nv-focus');
            focusEnter.append('g').attr('class', 'nv-x nv-axis');
            focusEnter.append('g').attr('class', 'nv-y1 nv-axis');
            focusEnter.append('g').attr('class', 'nv-y2 nv-axis');
            focusEnter.append('g').attr('class', 'nv-lines1Wrap');
            focusEnter.append('g').attr('class', 'nv-lines2Wrap');

            var contextEnter = gEnter.append('g').attr('class', 'nv-context');
            contextEnter.append('g').attr('class', 'nv-x nv-axis');
            contextEnter.append('g').attr('class', 'nv-y nv-axis');
            contextEnter.append('g').attr('class', 'nv-lines1Wrap');
            contextEnter.append('g').attr('class', 'nv-brushBackground');
            contextEnter.append('g').attr('class', 'nv-x nv-brush');

            // Legend
            var color_array = data.map(function(d,i) {
                return data[i].color || color(d, i);
            });

            if (showLegend) {
                legend.color(color_array);
                legend.width( availableWidth / 2 );

                g.select('.legendWrap')
                    .datum(data.map(function(series) {
                        series.originalKey = series.originalKey === undefined ? series.key : series.originalKey;
                        series.key = series.originalKey + (series.yAxis == 1 ? '' : ' (right axis)');
                        return series;
                    }))
                    .call(legend);

                if ( margin.top != legend.height()) {
                    margin.top = legend.height();
                    availableHeight1 = (height || parseInt(container.style('height')) || 400)
                        - margin.top - margin.bottom - height2;
                    availableHeight2 = height2 - margin2.top - margin2.bottom;
                    // availableHeight = (height || parseInt(container.style('height')) || 400)
                    //     - margin.top - margin.bottom;
                }

                g.select('.legendWrap')
                    .attr('transform', 'translate(' + ( availableWidth / 2 ) + ',' + (-margin.top) +')');
            }

            wrap.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

            // Main Chart Component(s)
            lines1
                .width(availableWidth)
                .height(availableHeight1)
                .color(color_array.filter(function(d,i) { return !data[i].disabled && data[i].yAxis == 1}));
            lines2
                .width(availableWidth)
                .height(availableHeight1)
                .color(color_array.filter(function(d,i) { return !data[i].disabled && data[i].yAxis == 2}));
            linesC
                .width(availableWidth)
                .height(availableHeight2)
                .color(color_array.filter(function(d,i) { return data[i].yAxis == 2}));

            g.select('.nv-context')
                .attr('transform', 'translate(0,' + ( availableHeight1 + margin.bottom + margin2.top) + ')')

            yScale1.domain(yDomain1 || d3.extent(series1, function(d) { return d.y } ))
                .range([0, availableHeight1]);

            yScale2.domain(yDomain2 || d3.extent(series2, function(d) { return d.y } ))
                .range([0, availableHeight1]);

            yScaleC.domain(yDomainC || d3.extent(series2, function(d) { return d.y } ))
                .range([availableHeight2, 0]);

            lines1.yDomain(yScale1.domain());
            lines2.yDomain(yScale2.domain());
            linesC.yDomain(yScaleC.domain());

            var context1LinesWrap = g.select('.nv-context .nv-lines1Wrap')
                .datum(dataLines2);

            if(dataLines2.length){d3.transition(context1LinesWrap).call(linesC);}

            // Setup Main (Focus) Axes
            xAxis
                .scale(x)
                .ticks( nv.utils.calcTicksX(availableWidth/100, dataLines1) )
                .tickSize(-availableHeight1, 0);

            y1Axis
                .ticks( nv.utils.calcTicksY(availableHeight1/36, dataLines1) )
                .tickSize( -availableWidth, 0);

            y2Axis
                .ticks( nv.utils.calcTicksY(availableHeight1/36, dataLines2) )
                .tickSize( -availableWidth, 0);

            g.select('.nv-focus .nv-x.nv-axis')
                .attr('transform', 'translate(0,' + availableHeight1 + ')');

            // Setup Brush
            brush
                .x(xC)
                .on('brush', function() {
                    //When brushing, turn off transitions because chart needs to change immediately.
                    var oldTransition = chart.duration();
                    chart.duration(0);
                    onBrush();
                    chart.duration(oldTransition);
                });

            if (brushExtent) brush.extent(brushExtent);

            var brushBG = g.select('.nv-brushBackground').selectAll('g')
                .data([brushExtent || brush.extent()])

            var brushBGenter = brushBG.enter()
                .append('g');

            brushBGenter.append('rect')
                .attr('class', 'left')
                .attr('x', 0)
                .attr('y', 0)
                .attr('height', availableHeight2);

            brushBGenter.append('rect')
                .attr('class', 'right')
                .attr('x', 0)
                .attr('y', 0)
                .attr('height', availableHeight2);

            var gBrush = g.select('.nv-x.nv-brush')
                .call(brush);
            gBrush.selectAll('rect')
                //.attr('y', -5)
                .attr('height', availableHeight2);
            gBrush.selectAll('.resize').append('path').attr('d', resizePath);

            onBrush();

            // Setup Secondary (Context) Axes
            xCAxis
                .scale(xC)
                .ticks( nv.utils.calcTicksX(availableWidth/100, dataLines2) )
                .tickSize(-availableHeight2, 0);

            g.select('.nv-context .nv-x.nv-axis')
                .attr('transform', 'translate(0,' + yScaleC.range()[0] + ')');
            d3.transition(g.select('.nv-context .nv-x.nv-axis'))
                .call(xCAxis);

            yCAxis
                .ticks( nv.utils.calcTicksY(availableHeight2/36, dataLines2) )
                .tickSize( -availableWidth, 0);

            d3.transition(g.select('.nv-context .nv-y.nv-axis'))
                .call(yCAxis);

            // g.select('.nv-context .nv-y.nv-axis').transition().duration(transitionDuration)
            //         .call(yCAxis);

            g.select('.nv-context .nv-x.nv-axis')
                .attr('transform', 'translate(0,' + yScaleC.range()[0] + ')');

            //============================================================
            // Event Handling/Dispatching (in chart's scope)
            //------------------------------------------------------------

            legend.dispatch.on('stateChange', function(newState) {
                for (var key in newState)
                    state[key] = newState[key];
                dispatch.stateChange(state);
                chart.update();
            });

            dispatch.on('tooltipShow', function(e) {
                if (tooltips) showTooltip(e, that.parentNode);
            });

            dispatch.on('changeState', function(e) {
                if (typeof e.disabled !== 'undefined') {
                    data.forEach(function(series,i) {
                        series.disabled = e.disabled[i];
                    });
                }
                chart.update();
            });

            //============================================================
            // Functions
            //------------------------------------------------------------

            // Taken from crossfilter (http://square.github.com/crossfilter/)
            function resizePath(d) {
                var e = +(d == 'e'),
                    x = e ? 1 : -1,
                    y = availableHeight2 / 3;
                return 'M' + (.5 * x) + ',' + y
                    + 'A6,6 0 0 ' + e + ' ' + (6.5 * x) + ',' + (y + 6)
                    + 'V' + (2 * y - 6)
                    + 'A6,6 0 0 ' + e + ' ' + (.5 * x) + ',' + (2 * y)
                    + 'Z'
                    + 'M' + (2.5 * x) + ',' + (y + 8)
                    + 'V' + (2 * y - 8)
                    + 'M' + (4.5 * x) + ',' + (y + 8)
                    + 'V' + (2 * y - 8);
            }


            function updateBrushBG() {
                if (!brush.empty()) brush.extent(brushExtent);
                brushBG
                    .data([brush.empty() ? xC.domain() : brushExtent])
                    .each(function(d,i) {
                        var leftWidth = xC(d[0]) - x.range()[0],
                            rightWidth = x.range()[1] - xC(d[1]);
                        d3.select(this).select('.left')
                            .attr('width',  leftWidth < 0 ? 0 : leftWidth);

                        d3.select(this).select('.right')
                            .attr('x', xC(d[1]))
                            .attr('width', rightWidth < 0 ? 0 : rightWidth);
                    });
            }


            function onBrush() {
                brushExtent = brush.empty() ? null : brush.extent();
                var extent = brush.empty() ? xC.domain() : brush.extent();

                //The brush extent cannot be less than one.  If it is, don't update the line chart.
                if (Math.abs(extent[0] - extent[1]) <= 1) {
                    return;
                }

                dispatch.brush({extent: extent, brush: brush});


                updateBrushBG();

                // Update Main (Focus)
                var focusLines1Wrap = g.select('.nv-focus .nv-lines1Wrap')
                    .datum(
                    dataLines1
                        .filter(function(d) { return !d.disabled })
                        .map(function(d,i) {
                            return {
                                key: d.key,
                                area: d.area,
                                values: d.values.filter(function(d,i) {
                                    return lines1.x()(d,i) >= extent[0] && lines1.x()(d,i) <= extent[1];
                                })
                            }
                        })
                );

                var focusLines2Wrap = g.select('.nv-focus .nv-lines2Wrap')
                    .datum(
                    dataLines2
                        .filter(function(d) { return !d.disabled })
                        .map(function(d,i) {
                            return {
                                key: d.key,
                                area: d.area,
                                values: d.values.filter(function(d,i) {
                                    return lines2.x()(d,i) >= extent[0] && lines2.x()(d,i) <= extent[1];
                                })
                            }
                        })
                );
                focusLines1Wrap.transition().duration(transitionDuration).call(lines1);
                focusLines2Wrap.transition().duration(transitionDuration).call(lines2);


                // Update Main (Focus) Axes
                g.select('.nv-focus .nv-x.nv-axis').transition().duration(transitionDuration)
                    .call(xAxis);
                g.select('.nv-focus .nv-y1.nv-axis').transition().duration(transitionDuration)
                    .call(y1Axis);
                g.select('.nv-focus .nv-y2.nv-axis')
                    .attr('transform', 'translate(' + x.range()[1] + ',0)')
                    .transition().duration(transitionDuration)
                    .call(y2Axis);
            }
        });

        return chart;
    }

    //============================================================
    // Event Handling/Dispatching (out of chart's scope)
    //------------------------------------------------------------

    lines1.dispatch.on('elementMouseover.tooltip', function(e) {
        e.pos = [e.pos[0] +  margin.left, e.pos[1] + margin.top];
        dispatch.tooltipShow(e);
    });

    lines1.dispatch.on('elementMouseout.tooltip', function(e) {
        dispatch.tooltipHide(e);
    });

    lines2.dispatch.on('elementMouseover.tooltip', function(e) {
        e.pos = [e.pos[0] +  margin.left, e.pos[1] + margin.top];
        dispatch.tooltipShow(e);
    });

    lines2.dispatch.on('elementMouseout.tooltip', function(e) {
        dispatch.tooltipHide(e);
    });

    dispatch.on('tooltipHide', function() {
        if (tooltips) nv.tooltip.cleanup();
    });

    //============================================================
    // Expose Public Variables
    //------------------------------------------------------------

    // expose chart's sub-components
    chart.dispatch = dispatch;
    chart.legend = legend;
    chart.lines1 = lines1;
    chart.lines2 = lines2;
    chart.linesC = linesC;
    chart.xAxis = xAxis;
    chart.y1Axis = y1Axis;
    chart.y2Axis = y2Axis;
    chart.xCAxis = xCAxis;
    chart.yCAxis = yCAxis;

    chart.options = nv.utils.optionsFunc.bind(chart);

    chart._options = Object.create({}, {
        // simple options, just get/set the necessary values
        width:      {get: function(){return width;}, set: function(_){width=_;}},
        height:     {get: function(){return height;}, set: function(_){height=_;}},
        focusHeight:     {get: function(){return height2;}, set: function(_){height2=_;}},
        showLegend: {get: function(){return showLegend;}, set: function(_){showLegend=_;}},
        yDomain1:      {get: function(){return yDomain1;}, set: function(_){yDomain1=_;}},
        yDomain2:    {get: function(){return yDomain2;}, set: function(_){yDomain2=_;}},
        yDomainC:    {get: function(){return yDomainC;}, set: function(_){yDomainC=_;}},
        brushExtent: {get: function(){return brushExtent;}, set: function(_){brushExtent=_;}},
        tooltips:    {get: function(){return tooltips;}, set: function(_){tooltips=_;}},
        tooltipContent:    {get: function(){return tooltip;}, set: function(_){tooltip=_;}},
        defaultState:    {get: function(){return defaultState;}, set: function(_){defaultState=_;}},
        noData:    {get: function(){return noData;}, set: function(_){noData=_;}},

        // options that require extra logic in the setter
        margin: {get: function(){return margin;}, set: function(_){
            margin.top    = _.top    !== undefined ? _.top    : margin.top;
            margin.right  = _.right  !== undefined ? _.right  : margin.right;
            margin.bottom = _.bottom !== undefined ? _.bottom : margin.bottom;
            margin.left   = _.left   !== undefined ? _.left   : margin.left;
        }},
        color:  {get: function(){return color;}, set: function(_){
            color = nv.utils.getColor(_);
            legend.color(color);
            // line color is handled above?
        }},
        interpolate: {get: function(){return lines1.interpolate();}, set: function(_){
            lines1.interpolate(_);
            lines2.interpolate(_);
            linesC.interpolate(_);
        }},
        xTickFormat: {get: function(){return xAxis.xTickFormat();}, set: function(_){
            xAxis.xTickFormat(_);
            xCAxis.xTickFormat(_);
        }},
        yTickFormat: {get: function(){return y1Axis.yTickFormat();}, set: function(_){
            y1Axis.yTickFormat(_);
            y2Axis.yTickFormat(_);
            yCAxis.yTickFormat(_);
        }},
        duration:    {get: function(){return transitionDuration;}, set: function(_){
            transitionDuration=_;
            y1Axis.duration(transitionDuration);
            y2Axis.duration(transitionDuration);
            yCAxis.duration(transitionDuration);
            xAxis.duration(transitionDuration);
        }},
        x: {get: function(){return lines.x();}, set: function(_){
            lines1.x(_);
            lines2.x(_);
            linesC.x(_);
        }},
        y: {get: function(){return lines.y();}, set: function(_){
            lines1.y(_);
            lines2.y(_);
            linesC.y(_);
        }}
    });

    nv.utils.initOptions(chart);

    return chart;
};