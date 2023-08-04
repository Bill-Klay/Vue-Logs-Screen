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
                <HelloWorld @changeStatus="loginButtonStatus"/>
                <v-btn 
                    :disabled="!validLogin" 
                    color="primary" 
                    title="With great power comes great responsibility">
                    Login
                </v-btn>
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
                        <v-btn color="purple" @click="isActive.value = false" :disabled="!validSignup">
                            Sign me up!
                        </v-btn>
                        <v-btn color="purple" @click="isActive.value = false">
                            Maybe Later?
                        </v-btn>
                        </v-card-actions>
                        </v-card>
                    </template>
                </v-dialog>
            </v-col>
            <v-col></v-col>
        </v-row>
        <v-row justify="center">
            <v-col cols="8">
                <div style="border: 1px solid grey; text-align: center;">
                    Made with <v-icon color="error" icon="mdi-heart"></v-icon> by yours truly using
                    <v-icon color="success" icon="mdi-vuejs"></v-icon> and
                    <v-icon color="primary" icon="mdi-vuetify"></v-icon> and
                    <v-icon color="warning" icon="mdi-language-python"></v-icon>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import HelloWorld from './HelloWorld.vue'
    export default {
        name: 'Login',
        components: {
            HelloWorld
        },
        data() {
            return {
                validLogin: false,
                validSignup: false,
                password: '',
                passwordRules: [
                    v => !!v || 'Password is required',
                    v => (v && v.length >= 8) || 'Password must be atleast 8 characters',
                ],
                email: '',
                emailRules: [
                    v => !!v || 'E-mail is required',
                    v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
                ],
                value: String,
            }
        },
        methods: {
            loginButtonStatus(newStatus) {
                this.validLogin = newStatus
            },
            signupButtonStatus(newStatus) {
                this.validSignup = newStatus
            }
        }
    }
</script>

<style>
    div {
        font-family: 'Victor Mono'
    }
</style>