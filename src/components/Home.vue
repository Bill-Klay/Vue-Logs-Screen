<template>
    <!-- application wireframe drawer navigation -->
    <v-layout class="rounded rounded-md">
        <v-navigation-drawer v-model="drawer">
            <v-list>
            <v-list-item title="Navigation drawer" class="text-center"></v-list-item>
            <v-list-item>
                <v-btn block color="#5dbea3">Compliance Monitoring</v-btn>
            </v-list-item>
            <v-list-item>
                <v-btn disabled block>Expense Monitoring Audit</v-btn>
            </v-list-item>
            <v-list-item>
                <v-btn color="error" @click="confirmLogout" block>Log Out</v-btn>
            </v-list-item>
            </v-list>
        </v-navigation-drawer>
        
        <!-- app bar -->
        <v-app-bar title="Compliance Monitoring" color="teal-darken-4" image="https://picsum.photos/1920/1080?random" scroll-behavior="fade-image" scroll-threshold="500">
            <template v-slot:image>
                <v-img gradient="to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)"></v-img>
            </template>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        </v-app-bar>
         
        <!-- main card for the home page displaying all the tables and selections  -->
        <v-main class="align-center justify-center">
            <v-row class="ma-6">
                <v-col cols="4"> 
                    <VueMultiselect class="mt-6" v-model="serverName" :options="serverOptions" placeholder="Select Server" label="name" track-by="name" @select="fetchDatabases" ></VueMultiselect>
                    <VueMultiselect class="mt-6" v-model="databaseName" :options="databaseOptions" placeholder="Select Database" @select="databaseConnection" ></VueMultiselect>
                    <v-row justify="space-between" class="mt-6">
                        <v-col cols="4">
                            <v-tooltip text="Fetch data for the selected database connection" location="bottom">
                                <template v-slot:activator="{ props }">
                                    <v-btn v-bind="props" color="success" elevation="5" @click="getData" block>Fetch</v-btn>
                                </template>
                            </v-tooltip>
                        </v-col>
                        <v-col cols="4">
                            <v-tooltip text="Publish the changes to the database" location="bottom">
                                <template v-slot:activator="{ props }">
                                    <v-btn v-bind="props" color="primary" elevation="5" @click="commitChanges"  block>Commit</v-btn>
                                </template>
                            </v-tooltip>
                        </v-col>
                        <v-col cols="4">
                            <v-tooltip text="Execute job steps" location="bottom">
                                <template v-slot:activator="{ props }">
                                    <v-btn v-bind="props" color="warning" elevation="5" @click="executeJob" block>Execute</v-btn>
                                </template>
                            </v-tooltip>
                        </v-col>
                    </v-row>
                </v-col>
                <v-col cols="6">
                    <!-- <v-img  :width="400" aspect-ratio="4/3" cover src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-img> -->
                    <v-table density="compact" class="pl-12 pr-12" v-if="dataCountItems.length">
                        <thead>
                        <tr>
                            <th class="text-left">
                            Table Name
                            </th>
                            <th class="text-left">
                            Count
                            </th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr
                            v-for="item in dataCountItems" :key="item.key">
                            <td>{{ item.key }}</td>
                            <td>{{ item.value }}</td>
                        </tr>
                        </tbody>
                    </v-table>
                </v-col>
                <v-col cols="2">
                    <v-img src="..\assets\Pandas_Black.png" style="max-width: 85%; max-height: 85%;" container/>
                    <!-- <v-img src="../assets/Pandas_Black.png" aspect-ratio="1" contain></v-img> -->
                    <v-row class="mt-6">
                        <v-btn class="white--text" color="#8B008B"  variant="outlined" block>Reset Workbench</v-btn>
                    </v-row>
                    <v-row class="mt-6">
                        <v-btn class="white--text" color="#8B008B" variant="outlined" block>Reset Defer</v-btn>
                    </v-row>
                </v-col>
            </v-row>
        </v-main>

        <!-- snack bars for the home page -->
        <v-snackbar v-model="snackExecution" :timeout="5000" :color="snackColor" variant="tonal">
            {{ snackMessage }}
            <template v-slot:actions>
                <v-btn
                    :color="snackColor"
                    variant="text"
                    v-if="isLogout" @click="logout">
                    Yes
                </v-btn>                
                <v-btn
                    :color="snackColor"
                    variant="text"
                    v-if="isLogout" @click="snackExecution = false">
                    No
                </v-btn>
                <v-btn
                    :color="snackColor"
                    variant="text"
                    v-else @click="closeSnack">
                    Okay
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
                backend: 'http://127.0.0.1:5000',
                isLogout: false,
                dataCountItems: []
            }
        },
        methods: {
            confirmLogout() {
                this.isLogout = true
                this.snackMessage = 'Do you want to logout?'
                this.snackColor = 'warning'
                this.snackExecution = true
            },
            logout() {
                localStorage.removeItem('token')
                this.$router.push('/login')
            },
            closeSnack() {
                this.snackExecution = false
            },
            databaseConnection() {
                const token = localStorage.getItem('token')
                if (!token) this.$router.push('/login')
                axios.put(this.backend + '/database', { db: this.databaseName }, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }).then(response => {
                    this.snackMessage = response.data.message
                    this.snackColor = response.data.color
                    this.snackExecution = true
                }).catch(error => {
                    console.log("Invalid request", error)
                })
            },
            fetchDatabases() {
                const token = localStorage.getItem('token') // replace 'token' with your actual key
                if (!token) this.$router.push('/login')

                if (!this.serverName || !this.serverName.ip) {
                    console.error('Server name or IP is not set')
                    return;
                }

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
            verifyDataFields() {
                if (!this.serverName || !this.databaseName) {
                    this.snackMessage = 'Select Database and Server'
                    this.snackColor = 'warning'
                    this.snackExecution = true
                    return false
                }
                else return true
            },
            getData() {
                if (this.verifyDataFields()) {
                    const token = localStorage.getItem('token')
                    if (!token) this.$router.push('/login')

                    axios.get(this.backend + '/database', {
                        headers: {
                        'Authorization': `Bearer ${token}`
                        }
                    }).then(response => {
                        this.dataCountItems = Object.entries(response.data).map(([key, value]) => ({ key, value }))
                        this.loading = true
                    }).catch(error => {
                        console.error(error)
                    })
                }
            },
            commitChanges() {
                if (this.verifyDataFields()) {
                    console.log("Changes will be comitted")
                }
            },
            executeJob() {
                if (this.verifyDataFields()) {
                    console.log("Job will be executed")
                }
            }
        }
    }
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>