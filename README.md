# ha-mcp23017-component
Manage ReefLed

# Installation via hacs 
1) open HACS
2) go to custom repositories and add:
    https://github.com/Elwinmage/ha-reefled-component


# Card

you need to install config-template-card and apexcharts-card from HACS

<code>
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
      name: clouds
      type: area
      color: rgb(100,100,100)
      yaxis_id: clouds
      curve: stepline
      data_generator: >
        const now = new Date();  now.setHours(0,0,0,0);  const data =[];
        data.push([now.getTime(),0]); var intensity=0;
        switch(entity.attributes.clouds.intensity){
          case "Low": 
            intensity = 1;
            break;
          case "Medium":
            intensity = 2;
            break;
          case "High":
            intensity = 3;
            break;
          default:
            intensity = 0;
            }
        data.push([now.getTime()+60000*(entity.attributes.clouds.from),intensity]);
        data.push([now.getTime()+60000*(entity.attributes.clouds.to),0]); return
        data;
    - entity: sensor.rsled160_2081858396_auto_1
      show:
        legend_value: false
      name: white
      color: rgb(200,200,200)
      yaxis_id: power
      data_generator: >
        const now = new Date(); now.setHours(0,0,0,0); const data = [];
        data.push([now.getTime(),0]);
        data.push([now.getTime()+60000*(entity.attributes.data.white.rise),0]);
        for (var point in entity.attributes.data.white.points){
          data.push([now.getTime()+60000*(entity.attributes.data.white.points[point].t+entity.attributes.data.white.rise),entity.attributes.data.white.points[point].i]);
          }
        data.push([now.getTime()+60000*(entity.attributes.data.white.set),0]);
        return data;
    - entity: sensor.rsled160_2081858396_auto_1
      show:
        legend_value: false
      name: blue
      color: rgb(100,100,250)
      yaxis_id: power
      data_generator: >
        const now = new Date(); now.setHours(0,0,0,0); const data = [];
        data.push([now.getTime(),0]);
        data.push([now.getTime()+60000*(entity.attributes.data.blue.rise),0]);
        for (var point in entity.attributes.data.blue.points){
          data.push([now.getTime()+60000*(entity.attributes.data.blue.points[point].t+entity.attributes.data.blue.rise),entity.attributes.data.blue.points[point].i]);
          }
        data.push([now.getTime()+60000*(entity.attributes.data.blue.set),0]);
        return data;
    - entity: sensor.rsled160_2081858396_auto_1
      show:
        legend_value: false
      name: moon
      color: rgb(250,100,250)
      yaxis_id: power
      data_generator: >
        const now = new Date(); now.setHours(0,0,0,0); const data = [];
        data.push([now.getTime(),0]);
        data.push([now.getTime()+60000*(entity.attributes.data.moon.rise),0]);
        for (var point in entity.attributes.data.moon.points){
          data.push([now.getTime()+60000*(entity.attributes.data.moon.points[point].t+entity.attributes.data.moon.rise),entity.attributes.data.moon.points[point].i]);
          }
        data.push([now.getTime()+60000*(entity.attributes.data.moon.set),0]);
        return data;
  yaxis:
    - id: clouds
      min: 0
      max: 3
      opposite: true
      apex_config:
        tickAmount: 3
        title:
          text: Cloud Cover Intensity
    - id: power
      min: 0
      max: 100
</code>
