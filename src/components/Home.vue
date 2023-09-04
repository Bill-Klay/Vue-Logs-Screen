<template>
    <v-layout class="rounded rounded-md">
        <v-navigation-drawer v-model="drawer">
            <v-list>
            <v-list-item title="Navigation drawer" class="text-center"></v-list-item>
            <v-list-item>
                <v-btn disabled block>Expense Monitoring Audit</v-btn>
            </v-list-item>
            <v-list-item>
                <v-btn color="error" @click="confirmLogout" block>Log Out</v-btn>
            </v-list-item>
            </v-list>
        </v-navigation-drawer>
  
        <v-app-bar title="Compliance Monitoring" color="teal-darken-4" image="https://picsum.photos/1920/1080?random" scroll-behavior="fade-image" scroll-threshold="500">
            <template v-slot:image>
                <v-img gradient="to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)"></v-img>
            </template>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        </v-app-bar>
  
        <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
            <v-row class="mt-2">
                <v-col cols="1"></v-col>
                <v-col cols="4"> 
                    <VueMultiselect class="mt-6" v-model="serverName" :options="serverOptions" placeholder="Select Server" label="name" track-by="name" @select="fetchDatabases" ></VueMultiselect>
                    <VueMultiselect class="mt-6" v-model="databaseName" :options="databaseOptions" placeholder="Select Database" ></VueMultiselect>
                </v-col>
                <v-col cols="5"></v-col>
                <v-col class="text-center mt-5 mr-1">
                    <img src="..\assets\Pandas_Black.png" style="max-width: 85%; max-height: 85%;"/>
                </v-col>
            </v-row>
        </v-main>

        <v-snackbar v-model="snackExecution" :timeout="5000" :color="snackColor" variant="outlined">
            {{ snackMessage }}
            <template v-slot:actions>
                <v-btn
                    :color="snackColor"
                    variant="text"
                    @click="logout">
                    Yes
                </v-btn>
                <v-btn
                    :color="snackColor"
                    variant="text"
                    @click="snackExecution = false">
                    No
                </v-btn>
            </template>
        </v-snackbar>
    </v-layout>
</template>

<script>
    import VueMultiselect from 'vue-multiselect'
    import axios from 'axios'

    export default {
        name: 'Home',
        components: {
            VueMultiselect
        },
        data() {
            return {
                serverOptions: [ 
                    { name: 'DEV', ip: '10.0.100.173' },
                    { name: 'QA', ip: '10.0.100.175' },
                    { name: 'STAGE', ip: '52.88.29.244' },
                    { name: 'PROD', ip: '44.229.141.215' }
                ],
                serverName: null,
                databaseOptions: [],
                databaseName: null,
                drawer: false,
                snackMessage: '',
                snackColor: '',
                snackExecution: false,
                backend: 'http://127.0.0.1:5000'
            }
        },
        methods: {
            confirmLogout() {
                this.snackMessage = 'Do you want to logout?'
                this.snackColor = 'warning'
                this.snackExecution = true
            },
            logout() {
                localStorage.removeItem('token')
                this.$router.push('/login')
            },
            fetchDatabases() {
                const token = localStorage.getItem('token') // replace 'token' with your actual key
                axios.get(this.backend + '/server?server=' + this.serverName.ip, {
                    headers: {
                    'Authorization': `Bearer ${token}`
                    }
                }).then(response => {
                    this.databaseOptions = Object.values(JSON.parse(response.data))
                }).catch(error => {
                    console.error(error)
                })
            },
        }
    }
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>