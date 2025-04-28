# Overview
RedSea Reefled Local Management (no cloud)

This is not an official repo of RedSea

Use at your own risk

# Installation via hacs 
1) open HACS
2) go to custom repositories and add:
    https://github.com/Elwinmage/ha-reefled-component

# Hardware
Test with the RESLED 160 but may work with 90 and 50 versions let me know.

If you have the RESLED Gen2 you can contact me to add the support

# What works
- Auto detect LED on private network (if on same network)
- Get and Set White, Blue and Moon values
- Get Fan and Temperature
- Get name and value for progams (with clouds support)
- Group and manage LED with a virtual device (Create a vitual device from the integration panel, then use the configure button to link the leds)

# Futur implementation
- Set programs (and implement the daily prog button that do nothing yet)
- Manage manual mode timing
- Random  program creation
- Daily program generation according to meteo of a specific place according to geographic coordinates

# Home Assitant Card
Here is an example to display your led programation.

<p align="center">                                                                                                                                                                              
  <img src="https://github.com/Elwinmage/ha-reefled-component/doc/img/program.png" alt="Image">                                                                                       
</p> 


You need to install decluttering, config-template-card and apexcharts-card from HACS.

Don't forget to edit the entity name to set your own.

<code>
decluttering_templates:
  reefled-auto:
    default:
      - icon: mdi:calendar
    card:
      type: custom:config-template-card
      entities:
        - - - sensor
      card:
        type: custom:apexcharts-card
        header:
          show: true
          title: ${'[[day_name]] :\ '+states[ '[[sensor]]' ].state}
          show_states: false
          colorize_states: false
        graph_span: 28h
        span:
          start: day
        series:
          - entity: '[[sensor]]'
            show:
              legend_value: false
            name: clouds
            type: area
            color: rgb(100,100,100)
            yaxis_id: clouds
            curve: stepline
            data_generator: >
              const now = new Date();   now.setHours(0,0,0,0);   const data=[];
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
              data.push([now.getTime()+60000*(entity.attributes.clouds.from%1440),intensity]);
              data.push([now.getTime()+60000*(entity.attributes.clouds.to%1440),0]);
              return data;
          - entity: '[[sensor]]'
            show:
              legend_value: false
            name: white
            color: rgb(200,200,200)
            yaxis_id: power
            data_generator: >
              const now = new Date();  now.setHours(0,0,0,0); const data = [];
              data.push([now.getTime(),0]);
              data.push([now.getTime()+60000*(entity.attributes.data.white.rise),0]);
              for (var point in entity.attributes.data.white.points){
                data.push([now.getTime()+60000*(entity.attributes.data.white.points[point].t+entity.attributes.data.white.rise),entity.attributes.data.white.points[point].i]);
                }
              data.push([now.getTime()+60000*(entity.attributes.data.white.set),0]);
              return data;
          - entity: '[[sensor]]'
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
          - entity: '[[sensor]]'
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
views:
  - title: Home
    sections:
      - type: grid
        cards:
          - type: heading
            heading: Nouvelle section
          - type: entities
            entities:
              - entity: switch.rsledXXXXXXXX_daily_prog
                name: Programmation journalière
          - type: conditional
            conditions:
              - condition: state
                entity: switch.rsledXXXXXXXX_daily_prog
                state: 'on'
            card:
              type: custom:decluttering-card
              template: reefled-auto
              variables:
                - sensor: sensor.rsledXXXXXXXX_lundi
                - day_name: Tous les jours
          - type: conditional
            conditions:
              - condition: state
                entity: switch.rsledXXXXXXXX_daily_prog
                state_not: 'on'
            card:
              type: custom:layout-card
              layout_type: custom:masonry-layout
              cards:
                - type: custom:decluttering-card
                  template: reefled-auto
                  variables:
                    - sensor: sensor.rsledXXXXXXXX_monday
                    - day_name: Monday
                - type: custom:decluttering-card
                  template: reefled-auto
                  variables:
                    - sensor: sensor.rsledXXXXXXXX_thuesday
                    - day_name: Thuesday
                - type: custom:decluttering-card
                  template: reefled-auto
                  variables:
                    - sensor: sensor.rsledXXXXXXXX_wednesday
                    - day_name: Wednesday
                - type: custom:decluttering-card
                  template: reefled-auto
                  variables:
                    - sensor: sensor.rsledXXXXXXXX_thrusday
                    - day_name: Thursday
                - type: custom:decluttering-card
                  template: reefled-auto
                  variables:
                    - sensor: sensor.rsledXXXXXXXX_friday
                    - day_name: Friday
                - type: custom:decluttering-card
                  template: reefled-auto
                  variables:
                    - sensor: sensor.rsledXXXXXXXX_saturday
                    - day_name: Saturday
                - type: custom:decluttering-card
                  template: reefled-auto
                  variables:
                    - sensor: sensor.rsledXXXXXXXX_sunday
                    - day_name: Sunday
</code>
