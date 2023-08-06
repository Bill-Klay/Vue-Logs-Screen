<template>
  <div>
    <v-text-field 
        v-model="password"
        :counter="8"
        :rules="passwordRules"
        label="Password"
        :append-icon="value ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append="() => (value = !value)"
        :type="value ? 'password' : 'text'"
        required>
    </v-text-field>

    <v-text-field 
        v-model="email"
        :rules="emailRules"
        label="E-mail"
        required>
    </v-text-field>
  </div>
</template>

<script>
    export default {
      name: 'HelloWorld',
      data() {
        return {
            password: '', // since password and email will change on each keypress they will need to be watched
            passwordRules: [
                v => !!v || 'Password is required',
                v => (v && v.length >= 8) || 'Password must be atleast 8 characters',
            ],
            email: '',
            emailRules: [
                v => !!v || 'E-mail is required',
                v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
            ],
            value: String
        }
      },
      watch: {
        password() { // event is emitted on each keypress
          this.$emit('changeStatus', { buttonStatus: this.password.length >= 8 && /.+@.+\..+/.test(this.email), username: this.email, password: this.password })
        },
        email() { // parent to child are props and child to parent are events
          this.$emit('changeStatus', { buttonStatus: this.password.length >= 8 && /.+@.+\..+/.test(this.email), username: this.email, password: this.password })
        }
      }
    }
</script>