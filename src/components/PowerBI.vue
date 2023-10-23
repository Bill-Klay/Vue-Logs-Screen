<template>
    <!-- application wireframe drawer navigation -->
    <v-layout class="rounded rounded-md">
        <v-navigation-drawer v-model="drawer">
            <v-list>
            <v-list-item title="Navigation drawer" class="text-center"></v-list-item>
            <v-list-item>
                <v-btn block color="#5dbea3" @click="compliance">Compliance Monitoring</v-btn>
            </v-list-item>
            <v-list-item>
                <v-btn block color="#a881af" active>Power BI</v-btn>
            </v-list-item>
            <v-list-item>
                <v-btn disabled block>Expense Monitoring Audit</v-btn>
            </v-list-item>
            <v-list-item>
                <v-btn color="error" @click="confirmLogout" block>Log Out</v-btn>
            </v-list-item>
            <v-list-item>
                <v-switch v-model="toggleValue" hide-details true-value="ChatGPT" false-value="Power BI" color="warning" :label="`${toggleValue}`" inset></v-switch>
            </v-list-item>
            </v-list>
        </v-navigation-drawer>
        
        <!-- app bar -->
        <v-app-bar title="Ask your data" color="teal-darken-4" image="https://picsum.photos/1920/1080?random" scroll-behavior="fade-image" scroll-threshold="500">
            <template v-slot:image>
                <v-img gradient="to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)"></v-img>
            </template>
            <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        </v-app-bar>
         
        <!-- main card for the home page displaying all the tables and selections  -->
        <v-main class="align-center justify-center">
            <!-- <iframe title="IndustryData_Analyses_QandA" width="100%" height="100%" src="https://app.powerbi.com/reportEmbed?reportId=c9cdae98-7661-4669-8f84-2beedf742acc&autoAuth=true&ctid=026e0585-0f6d-4eb2-ba93-8c4a4d4883c4" frameborder="0" allowFullScreen="true"></iframe> -->
            <PowerBIQnaEmbed style="width:100vw; height:90vh;" :embedConfig="embedConfig" ref="qnaEmbed" v-if="toggleValue == 'Power BI'"></PowerBIQnaEmbed>
            <template v-else>
                <v-row class="ma-6">
                    <v-col cols="3"></v-col>
                    <v-col>
                        <v-file-input v-model="file" color="deep-purple-accent-4" label="Upload File" prepend-icon="mdi-paperclip" variant="outlined" accept=".xls,.xlsx,.csv" show-size></v-file-input>
                        <v-btn @click="uploadFile">Upload File</v-btn>
                    </v-col>
                    <v-col cols="3"></v-col>
                </v-row>
                <v-row class="ma-6" :justify="message.speaker ? 'start' : 'end'"
                v-for="message in messages" :key="message.id">
                    <v-card>
                        <v-card-text v-if="isSingleValue(message.text)">
                            {{ message.text }}
                        </v-card-text>
                        <v-card-text v-else>
                            <EasyDataTable :headers="th(message.text)" :items="td(message.text)"/>
                        </v-card-text>
                    </v-card>
                </v-row>
                <v-row class="ma-6">
                    <v-col cols="2"></v-col>
                    <v-col>
                        <v-text-field v-model="newMessage" @keyup.enter="sendMessage(true)" label="Enter your query..." hint="For example: What is the total count?"></v-text-field>
                    </v-col>
                    <v-col cols="2"></v-col>
                </v-row>
            </template>
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
    import { PowerBIQnaEmbed } from 'powerbi-client-vue-js';
    import { models } from 'powerbi-client';
    import axios from 'axios';

    export default {
        name: 'PowerBI',
        components: {
            PowerBIQnaEmbed
        },
        data() {
            return {
                embedConfig: {
                    type: "report",
                    id: "c9cdae98-7661-4669-8f84-2beedf742acc",
                    embedUrl: "https://app.powerbi.com/reportEmbed?reportId=c9cdae98-7661-4669-8f84-2beedf742acc&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVVTLU5PUlRILUNFTlRSQUwtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQiLCJlbWJlZEZlYXR1cmVzIjp7InVzYWdlTWV0cmljc1ZOZXh0Ijp0cnVlfX0%3d",
                    accessToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSIsImtpZCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMDI2ZTA1ODUtMGY2ZC00ZWIyLWJhOTMtOGM0YTRkNDg4M2M0LyIsImlhdCI6MTY5ODA0NTEyNywibmJmIjoxNjk4MDQ1MTI3LCJleHAiOjE2OTgwNTA4MjAsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVlFBcS84VUFBQUFqRDUxUjlHd3pJa2hWQWZtblI1N3Njd0p1dXJRcDdtUDVMNkpnZ1NzUFBqaGVZMlNXWDUvN05Pamw0OFZHdktuVzZHM3R3WWpkVU1LVWVQamtleUVyOUpHYXlNMUZ0c1BSaUZMelgvbGtIYz0iLCJhbXIiOlsicHdkIiwicnNhIiwibWZhIl0sImFwcGlkIjoiODcxYzAxMGYtNWU2MS00ZmIxLTgzYWMtOTg2MTBhN2U5MTEwIiwiYXBwaWRhY3IiOiIwIiwiZGV2aWNlaWQiOiI1N2Y1MzlkMC1jYWZkLTRjNmEtYTFiOC1mYmQ1MGFjYTk5ZDAiLCJmYW1pbHlfbmFtZSI6IktoYW4iLCJnaXZlbl9uYW1lIjoiTXVoYW1tYWQgQmlsYWwiLCJpcGFkZHIiOiIxMDMuNy42MC43NiIsIm5hbWUiOiJNdWhhbW1hZCBCaWxhbCBLaGFuIiwib2lkIjoiMjIyMGJhYTktOWRlNy00ZTFkLThlYmEtZjNkNmU3MzQwMTFkIiwicHVpZCI6IjEwMDMyMDAwRjA3NkE1NjgiLCJyaCI6IjAuQVhjQWhRVnVBbTBQc2s2Nms0eEtUVWlEeEFrQUFBQUFBQUFBd0FBQUFBQUFBQUIzQUpvLiIsInNjcCI6InVzZXJfaW1wZXJzb25hdGlvbiIsInNpZ25pbl9zdGF0ZSI6WyJrbXNpIl0sInN1YiI6Im4wWjFzM0VfY0Y0TjZTZUpkdUNIMVdtS2lHN2Z5MWlFaVlYWml2OThlc2ciLCJ0aWQiOiIwMjZlMDU4NS0wZjZkLTRlYjItYmE5My04YzRhNGQ0ODgzYzQiLCJ1bmlxdWVfbmFtZSI6ImJpbGFsLmtoYW5AcW9yZGF0YS5jb20iLCJ1cG4iOiJiaWxhbC5raGFuQHFvcmRhdGEuY29tIiwidXRpIjoiUnJVdThGZkh2a2VqNTFld0pXWmpBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il19.s4R7lDtRwFWwUZt6v1OhcJeHz_Fdd78wKigZFCvUaSMGx9F3djhujE5uoi49KAUfpzbOMESoRknb9TAS9ltdlH_r5XyuAsvhCrTVIvpIKSi38ar0oDyid2Ga8lGc7Lt4JRq1px-MW-gpKxDRN6sNZ8LD7RMrYbrSbItJh1mUpE5jIl5quPO5Yp9exTDdF8Hbylkz2hQx9ywT4acmc8X7ybTKrqCMISN2G2n7vsT7mEBdri11Iky2YOswlniXr2hqu626YK5FSaaflXW717ChLcz3qYwAt-ro5JNtTe8q_15c1-rY392ADAybPZuYdKoFnPU6B4TE8V-fF8qiEcdA0A",
                    datasetIds: ["e2343861-7dde-4f5a-a024-a79a613589d2"],
                    tokenType: models.TokenType.Aad,
                    // hostname: "https://app.powerbi.com",
                    viewMode: models.QnaMode.Interactive,
                    settings: {
                        panes: {
                            filters: {
                                expanded: false,
                                visible: false
                            }
                        },
                        // background: models.BackgroundType.Transparent,
                        filterPaneEnabled: true,
                        navContentPaneEnabled: false,
                        visualRenderedEvents: false // Because visuals might render due to user interactions, it's recommended that this event only be turned on when needed.
                    }
                },
                drawer: false,
                snackMessage: '',
                snackColor: '',
                snackExecution: false,
                isLogout: false,
                report: null,
                backend: 'http://127.0.0.1:5000',
                toggleValue: 'Power BI',
                file: null,
                messages: [
                    { id: 1, text: 'Hello!', speaker: true}, // 1 is the user 0 is the server
                    { id: 2, text: 'Hello from the other side!', speaker: false},
                ],
                newMessage: '',
                headers: [],
                items: []
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
            compliance() {
                this.$router.push('/home')
            },
            uploadFile() {
                if (this.file) {
                    console.log(this.file[0])
                    let formData = new FormData()
                    formData.append('file', this.file[0])
                    console.log(formData)
                    axios.put(this.backend + "/powerbi", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                    }).then(
                    response => {
                        console.log(response.data);
                    },
                    error => {
                        console.log(error);
                    }
                    );
                }
                else console.log("There are no files")
            },
            sendMessage() {
                if (this.newMessage.trim() !== '') {
                    this.messages.push({
                        id: this.messages.length + 1,
                        text: this.newMessage,
                        speaker: 1
                    })
                    axios.post(this.backend + '/powerbi', { prompt: this.newMessage }).then(response => {
                        this.messages.push({
                            id: this.messages.length + 1,
                            text: response.data,
                            speaker: 0
                        })
                    }).catch(error => {
                        console.log("Invalid request", error)
                    })
                    this.newMessage = ''
                }
            },
            isSingleValue(msg) {
                if(typeof msg == 'string' || typeof msg == 'number') return true
                else return false
            },
            th(msg) {
                // Get the keys of the first item
                const keys = Object.keys(msg[0]);

                // Map the keys to header objects
                return keys.map(key => ({
                text: key.toUpperCase(),
                value: key
                }));
            },
            td(msg) {
                return msg
            }
        }
    }
</script>