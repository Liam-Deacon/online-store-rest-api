<template>
  <div>
  <h3>Welcome</h3>
  <p>
    Please provide some information about you so that we can provide you
    with the best experience.
  </p>
  <!-- <h4>{{ title }}</h4> -->
  <v-stepper
    v-model="i_step"
    vertical
  >
    <v-stepper-step v-bind:complete="i_step > 1" step="1">
      Basic Information
    </v-stepper-step>

    <v-stepper-content step="1">
      <v-card
        class="mb-12"
        color="grey lighten-1"
        height="200px"
      ></v-card>

      <v-btn color="primary" @click="i_step = 2">Continue</v-btn>
      <v-btn text>Cancel</v-btn>
    </v-stepper-content>

    <v-divider></v-divider>

    <v-stepper-step v-bind:complete="i_step > 2" step="2">
      About Your Big Day
    </v-stepper-step>

    <v-stepper-content step="2">
      <v-card
        class="mb-12"
        color="grey lighten-1"
        height="200px"
      ></v-card>

      <v-btn color="primary" @click="i_step = 3">Continue</v-btn>
      <v-btn text>Cancel</v-btn>
    </v-stepper-content>

    <v-divider></v-divider>

    <v-stepper-step step="3">
      Gift Preferences
    </v-stepper-step>

    <v-stepper-content step="3">
      <v-card
        class="mb-12"
        color="grey lighten-1"
        height="200px"
      ></v-card>

      <v-btn color="primary" @click="i_step = 4">Complete</v-btn>
      <v-btn text>Cancel</v-btn>
    </v-stepper-content>

  </v-stepper>
  </div>
</template>

<script>
export default {
  data () {
    return {
      i_step: 1,
      title: function () {
        let options = ['Basic Information', 'About Your Big Day', 'Gift Preferences']
        return options[this.i_step]
      }
    }
  }
}
</script>
