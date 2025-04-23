# ha-mcp23017-component
Manage ReefLed

# Installation via hacs 
1) open HACS
2) go to custom repositories and add:
    https://github.com/Elwinmage/ha-reefled-component


# Card

type: custom:config-template-card
entities:
  - sensor.rsled160_2081858396_auto_1
card:
  type: custom:apexcharts-card
  header:
    show: true
    title: ${states['sensor.rsled160_2081858396_auto_1'].state}
    show_states: false
    colorize_states: false
  graph_span: 28h
  span:
    start: day
  series:
    - entity: sensor.rsled160_2081858396_auto_1
      show:
        legend_value: false
      name: white
      color: rgb(200,200,200)
      data_generator: >
        const now = new Date(); now.setHours(0,0,0,0); const data = [];
        data.push([now.getTime(),0]);
        data.push([now.getTime()+60000*(entity.attributes.white.rise),0]); for
        (var point in entity.attributes.white.points){
          data.push([now.getTime()+60000*(entity.attributes.white.points[point].t+entity.attributes.white.rise),entity.attributes.white.points[point].i]);
          }
        data.push([now.getTime()+60000*(entity.attributes.white.set),0]); return
        data;
    - entity: sensor.rsled160_2081858396_auto_1
      show:
        legend_value: false
      name: blue
      color: rgb(100,100,250)
      data_generator: >
        const now = new Date(); now.setHours(0,0,0,0); const data = [];
        data.push([now.getTime(),0]);
        data.push([now.getTime()+60000*(entity.attributes.blue.rise),0]); for
        (var point in entity.attributes.blue.points){
          data.push([now.getTime()+60000*(entity.attributes.blue.points[point].t+entity.attributes.white.rise),entity.attributes.blue.points[point].i]);
          }
        data.push([now.getTime()+60000*(entity.attributes.blue.set),0]); return
        data;
    - entity: sensor.rsled160_2081858396_auto_1
      show:
        legend_value: false
      name: moon
      color: rgb(250,100,250)
      data_generator: >
        const now = new Date(); now.setHours(0,0,0,0); const data = [];
        data.push([now.getTime(),0]);
        data.push([now.getTime()+60000*(entity.attributes.moon.rise),0]); for
        (var point in entity.attributes.moon.points){
          data.push([now.getTime()+60000*(entity.attributes.moon.points[point].t+entity.attributes.moon.rise),entity.attributes.moon.points[point].i]);
          }
        data.push([now.getTime()+60000*(entity.attributes.moon.set),0]); return
        data;
