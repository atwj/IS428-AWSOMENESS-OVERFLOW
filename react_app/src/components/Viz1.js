import React, { Component } from 'react';
import * as d3 from 'd3';
import './Viz1.css'




class Chart1 extends Component {
    constructor(props) {
        super(props)
        this.dr = 4
        this.off = 20
        this.collapse = {}
        this.group = []
        this.net = {}
        this.createBarChart = this.createBarChart.bind(this)
        this.nodeid = this.nodeid.bind(this)
        this.linkid = this.linkid.bind(this)
        this.tick = this.tick.bind(this)

        // this.createGraph = this.createGraph.bind(this)
    }
    componentDidMount() {
        this.createBarChart()
        // this.createGraph()
    }
    componentDidUpdate() {
        this.createBarChart()
        // this.createGraph()
    }

    getGroup(n){return n.group}

    network(data, prev, index, collapse){
        collapse = collapse || {}
        let gm = {},    // group map
            nm = {},    // node map
            lm = {},    // link map
            gn = {},    // previous group nodes
            gc = {},    // previous group centroids
            nodes = [], // output nodes
            links = []  // output links

        // process previous nodes for reuse or centroid calculation
        if (typeof prev.nodes != 'undefined') {
            prev.nodes.forEach(n => {
                let i = index(n), o
                if (n.size > 0 ){
                    gn[i] = n
                    n.size = 0
                } else {
                    o = gc[i] || (gc[i] = { x: 0, y: 0, count: 0 })
                    o.x += n.x
                    o.y += n.y
                    o.count += 1
                }
            })
        }

        // determine nodes
        for (let k = 0; k < data.nodes.length; ++k) {

            let n = data.nodes[k],
                i = index(n),
                l = gm[i] || (gm[i] = gn[i]) || (gm[i] = { group: i, size: 0, nodes: [] })

            if (collapse[i] !== true) {
                // the node should be directly visible
                nm[n.name] = nodes.length
                nodes.push(n)
                if (gn[i]) {
                    // place new nodes at cluster location (plus jitter)
                    n.x = gn[i].x + Math.random();
                    n.y = gn[i].y + Math.random();
                }
            } else {
                // the node is part of a collapsed cluster
                if (l.size == 0) {
                    // if new cluster, add to set and position at centroid of leaf nodes
                    nm[i] = nodes.length
                    nodes.push(l)
                    if (gc[i]) {
                        l.x = gc[i].x / gc[i].count
                        l.y = gc[i].y / gc[i].count
                    }
                }
                l.nodes.push(n)
            }
            // always count group size as we also use it to tweak the force graph strengths/distances
            l.size += 1
            n.group_data = l
        }
        for (let i in gm) {
            gm[i].link_count = 0; this.group.push(gm[i].group);
        }

        for (let k = 0; k < data.links.length; ++k) {
            let e = data.links[k],
                u = index(e.source),
                v = index(e.target)
            if (u != v) {
                gm[u].link_count++
                gm[v].link_count++
            }
            u = !collapse[u] ? nm[e.source.name] : nm[u];
            v = !collapse[v] ? nm[e.target.name] : nm[v];
            let i = (u < v ? u + "|" + v : v + "|" + u),
                l = lm[i] || (lm[i] = { source: u, target: v, size: 0 });
            l.size += 1;
        }
        for (let i in lm) { links.push(lm[i]); }
        return {nodes: nodes, links: links}
    }

    convexHulls(nodes, index, offset) {
        let hulls = {}

        // create point sets
        for (let k = 0; k < nodes.length; ++k) {
            let n = nodes[k]
            if (n.size) continue;
            let i = index(n),
                l = hulls[i] || (hulls[i] = [])
            l.push([n.x - offset, n.y - offset]);
            l.push([n.x - offset, n.y + offset]);
            l.push([n.x + offset, n.y - offset]);
            l.push([n.x + offset, n.y + offset]);
        }

        // creates convex hulls
        var hullset = [];
        for (let i in hulls) {
            hullset.push({ group: i, path: d3.polygonHull(i)});
        }
        return hullset
    }


    drawCluster(d) {
        return d3.line(d.path).curve(d3.curveCardinal.tension(.85))
    }

    nodeid(n) {
        return n.size ? "_g_" + n.group : n.name;
    }

    linkid(l) {
        var u = this.nodeid(l.source),
            v = this.nodeid(l.target);
        return u < v ? u + "|" + v : v + "|" + u;
    }

    tick() {
        path.attr("d", function (d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0 1," + d.target.x + "," + d.target.y;
        });

        circle.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });

        text.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    }

    createBarChart() {
        const node = this.node
        let data = this.props.data
        for (let i = 0; i < data.links.length; ++i){
            let o = data.links[i]
            o.source = data.nodes[o.source]
            o.target = data.nodes[o.target]
        }
        let hullg = d3.select(node).append('g')
        let linkg = d3.select(node).append('g')
        let nodeg = d3.select(node).append('g')


        d3.select(node).selectAll(".mytext")
            .data(data.nodes)
            .enter()
            .append('text')
            .text(d=> d.name)
            .style("text-anchor", "middle")
            .style("fill", "#555")
            .style("font-family", "Arial")
            .style("font-size", function (d) { return d.nodesize > 80 ? 28 : 12 })
            .style("visibility", "visible");

        let net = this.network(data, this.net, this.getGroup, this.collapse)

        let simulation = d3.forceSimulation()
            .force("link", d3.forceLink())

        simulation.nodes(net.nodes)
            .on("tick", tick)

        simulation.force("link")
            .links(net.nodes)

        hullg.selectAll("path.hull")
            .remove()
        hullg.selectAll("path.hull")
            .data(this.convexHulls(net.nodes, this.getGroup, this.off))
            .enter().append('path')
            .attr("class", "hull")
            .attr("id", function (d) { return (d.group); })
            .attr("d", this.drawCluster)
            .style("fill", (d) => d3.scaleLinear(d3.schemeCategory20)(d.group))
            .style("visibility", "visible")

        let link = linkg.selectAll("line.link").data(net.links, this.linkid);
        link.exit().remove();
        link.enter().append("line")
            .attr("class", "link")
            .attr("x1", function (d) { return d.source.x; })
            .attr("y1", function (d) { return d.source.y; })
            .attr("x2", function (d) { return d.target.x; })
            .attr("y2", function (d) { return d.target.y; })
            .style("stroke-width", function (d) { return d.size || 1; })
            .style("visibility", "visible")
            .attr("opacity", 0.5);

        let _node = nodeg.selectAll("circle.node").data(net.nodes, this.nodeid);
        _node.exit().remove();
        _node.enter().append("circle")
        // if (d.size) -- d.size > 0 when d is a group node.
        // .attr("class", function (d) { return "node" + (d.size ? "" : " leaf"); })
            .attr("class", function (d) { return "node" + d.group; })
            // .attr("r", function (d) { console.log(d.nodesize); return d.size ? d.size + dr : dr + 1; })
            //.attr("r", function (d) { return d.nodesize ? ((d.nodesize / 7036.41) * 100) : dr + 1; })
            .attr("r", function (d) { return d.nodesize > 80 ? d.nodesize / 2 : 5 })
            .attr("cx", function (d) { return d.x; })
            .attr("cy", function (d) { return d.y; })
            .style("fill", d => d3.scaleLinear(d3.schemeCategory20)(d.group))
            .style("visibility", "visible");
        /*const dataMax = max(this.props.data)
        const yScale = scaleLinear()
            .domain([0, dataMax])
            .range([0, this.props.size[1]])
        select(node)
            .selectAll('rect')
            .data(this.props.data)
            .enter()
            .append('rect')

        select(node)
            .selectAll('rect')
            .data(this.props.data)
            .exit()
            .remove()

        select(node)
            .selectAll('rect')
            .data(this.props.data)
            .style('fill', '#fe9922')
            .attr('x', (d,i) => i * 25)
            .attr('y', d => this.props.size[1] — yScale(d))
    .attr('height', d => yScale(d))
            .attr('width', 25)
            */
    }

    render() {
        return (
            <svg ref={node => this.node = node}
                    width={this.props.size[0]} height={this.props.size[1]}>
            </svg>
        );
    }
}

export default Chart1;