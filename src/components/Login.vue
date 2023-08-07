<template>
    <v-container>
        <v-row class="mt-5 mb-16">
            <v-col></v-col>
            <v-col>
                <v-row>
                    <v-col cols="4">
                        <img src="..\assets\Pandas_Black.png" style="max-width: 100%; max-height: 100%; margin-top: 20px;"/>
                    </v-col>
                    <v-col cols="4">
                        <img src="..\assets\qordata_logo.png" style="margin-top: 100%; position: relative; max-height: 27%;"/>
                    </v-col>
                </v-row>
                <HelloWorld @changeStatus="loginButtonStatus"/> <!-- the child event is captured here -->
                <v-tooltip text="With great power comes great responsibility" location="bottom">
                    <template v-slot:activator="{ props }">
                        <v-btn v-bind="props" :disabled="!validLogin" color="primary" @click="login">
                            Login
                        </v-btn>
                    </template>
                </v-tooltip>
                <v-dialog transition="dialog-top-transition" width="40%">
                    <template v-slot:activator="{ props }">
                    <a v-bind="props" style="margin-left: 5%; cursor: pointer; color: purple;">
                        New to compliance monitoring?
                    </a>
                    </template>
                    <template v-slot:default="{ isActive }">
                        <v-card>
                            <v-toolbar color="purple" title="Welcome to the team!"></v-toolbar>
                            <v-card-text>
                                <HelloWorld @changeStatus="signupButtonStatus"/>
                            </v-card-text>
                            <v-card-actions class="justify-end">
                                <v-btn color="purple" @click="signup(); isActive.value = false" :disabled="!validSignup">
                                    Sign me up!
                                </v-btn>
                                <v-btn color="purple" @click="isActive.value = false">
                                    Maybe Later?
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </template>
                </v-dialog>
                <v-snackbar v-model="snackExecution" :timeout="3000" :color="snackColor" variant="outlined">
                    {{ snackMessage }}
                    <template v-slot:actions>
                        <v-btn
                            :color="snackColor"
                            variant="text"
                            @click="snackExecution = false">
                            Close
                        </v-btn>
                    </template>
                </v-snackbar>
            </v-col>
            <v-col></v-col>
        </v-row>
        <v-row justify="center" v-if="false">
            <v-col cols="8">
                <div style="border: 1px solid grey; text-align: center; color: grey;">
                    Made with <v-icon color="error" icon="mdi-heart"></v-icon> by yours truly -
                    <v-icon color="success" icon="mdi-vuejs"></v-icon>
                    <v-icon color="primary" icon="mdi-vuetify"></v-icon>
                    <v-icon color="warning" icon="mdi-language-python"></v-icon> - don't forget to star the repo
                    <a href="https://github.com/Bill-Klay/Vue-Logs-Screen"><v-icon icon="mdi-github"></v-icon></a>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import HelloWorld from './HelloWorld.vue'
    import axios from 'axios'

    export default {
        name: 'Login',
        username: '', // no need to place these credentials values in the return scope
        password: '', // since value is returned here from child
        components: {
            HelloWorld
        },
        data() {
            return {
                validLogin: false,
                validSignup: false,
                snackMessage: '',
                snackColor: '',
                snackExecution: false,
                backend: 'http://127.0.0.1:5000' // but this value needs to declared when the instance is created
            }
        },
        methods: {
            loginButtonStatus(payLoad) { // the emited event from the child captured here
                this.validLogin = payLoad.buttonStatus
                this.username = payLoad.username
                this.password = payLoad.password
            },
            signupButtonStatus(payLoad) {
                this.validSignup = payLoad.buttonStatus
                this.username = payLoad.username
                this.password = payLoad.password
            },
            signup() {
                this.validSignup = false
                axios.post(this.backend + '/register', { username: this.username, password: this.password }).then(response => {
                    this.snackMessage = response.data.message
                    this.snackColor = response.data.color
                    this.snackExecution = true
                }).catch(error => {
                    console.log("Invalid request", error)
                })
            },
            login() {
                axios.post(this.backend + '/login', { username: this.username, password: this.password }).then(response => {
                    this.snackMessage = response.data.message
                    this.snackColor = response.data.color
                    this.snackExecution = true
                    if(response.data.access_token) {
                        localStorage.setItem('token', response.data.access_token)
                        this.$router.push('/home')
                    }
                }).catch(error => {
                    console.log("Invalid request", error)
                })
            }
        }
    }
</script>