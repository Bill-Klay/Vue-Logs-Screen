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
        <v-main class="align-center justify-center" id="myPowerbi">
            <!-- <iframe title="IndustryData_Analyses_QandA" width="100%" height="100%" src="https://app.powerbi.com/reportEmbed?reportId=c9cdae98-7661-4669-8f84-2beedf742acc&autoAuth=true&ctid=026e0585-0f6d-4eb2-ba93-8c4a4d4883c4" frameborder="0" allowFullScreen="true"></iframe> -->
            <PowerBIQnaEmbed style="width:100vw; height:90vh;" :embedConfig="embedConfig" ref="qnaEmbed"></PowerBIQnaEmbed>
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
                    accessToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSIsImtpZCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMDI2ZTA1ODUtMGY2ZC00ZWIyLWJhOTMtOGM0YTRkNDg4M2M0LyIsImlhdCI6MTY5NzY5OTA5MCwibmJmIjoxNjk3Njk5MDkwLCJleHAiOjE2OTc3MDM5MDAsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVlFBcS84VUFBQUFwSGo4dVBFVXJLVXRlbnpNMlc4WlZ5cGdaNlVtZFlqS2V6TWRqZ0Vrd3N1dGVKU2dreCszUWp1NVg2TVBEdGdETlVwUkVaRTYrZHZ2NlJ3cVljMkxmOHpmQklGM3RIZlpobitEczRnbjFZUT0iLCJhbXIiOlsicHdkIiwicnNhIiwibWZhIl0sImFwcGlkIjoiODcxYzAxMGYtNWU2MS00ZmIxLTgzYWMtOTg2MTBhN2U5MTEwIiwiYXBwaWRhY3IiOiIwIiwiZGV2aWNlaWQiOiI1N2Y1MzlkMC1jYWZkLTRjNmEtYTFiOC1mYmQ1MGFjYTk5ZDAiLCJmYW1pbHlfbmFtZSI6IktoYW4iLCJnaXZlbl9uYW1lIjoiTXVoYW1tYWQgQmlsYWwiLCJpcGFkZHIiOiIxMDMuNy42MC43NiIsIm5hbWUiOiJNdWhhbW1hZCBCaWxhbCBLaGFuIiwib2lkIjoiMjIyMGJhYTktOWRlNy00ZTFkLThlYmEtZjNkNmU3MzQwMTFkIiwicHVpZCI6IjEwMDMyMDAwRjA3NkE1NjgiLCJyaCI6IjAuQVhjQWhRVnVBbTBQc2s2Nms0eEtUVWlEeEFrQUFBQUFBQUFBd0FBQUFBQUFBQUIzQUpvLiIsInNjcCI6InVzZXJfaW1wZXJzb25hdGlvbiIsInNpZ25pbl9zdGF0ZSI6WyJrbXNpIl0sInN1YiI6Im4wWjFzM0VfY0Y0TjZTZUpkdUNIMVdtS2lHN2Z5MWlFaVlYWml2OThlc2ciLCJ0aWQiOiIwMjZlMDU4NS0wZjZkLTRlYjItYmE5My04YzRhNGQ0ODgzYzQiLCJ1bmlxdWVfbmFtZSI6ImJpbGFsLmtoYW5AcW9yZGF0YS5jb20iLCJ1cG4iOiJiaWxhbC5raGFuQHFvcmRhdGEuY29tIiwidXRpIjoicmV5Szk4Ulg5MDZoM0JsZFhnNEFBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il19.TAaR1wqzOiyhcRgMRdFzM9CM57f4dH1PwLwk00TPkdV65TPSCo-36v_wk_T-B5mRkB6N1Tvonps2NlMl0vEoWKITyfspySyOGlzBHRUsorYNbca_BlAHXWSEYXQX4KVwgNKiC1Y9K4gX9sn1E9-0ZzpbowEM0EMpv4Xh1_b18UYO4LVZrQGedhwe6D9KiTR5VfzYEwYyHuLFhJp8l_rfWSevwLWgAbhGWbyviJmtlySKgyZkFGuZXl6xbLnvCwSi53MalaV8sDeRX52Zjh8OcQnVYa-lASPmnHGdKDKBfAM8ofayb1r8yqUyHnkHiTfUOeDmYkwpXARiZScR8gpyug",
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
            }
        }
    }
</script>