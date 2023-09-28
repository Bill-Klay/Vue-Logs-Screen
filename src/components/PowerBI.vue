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
                <v-btn block color="#a881af" dark active>Power BI</v-btn>
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
        <v-main class="align-center justify-center" >
            <!-- <iframe title="HR_Leave_Analyses_QandA" width="100%" height="100%" src="https://app.powerbi.com/reportEmbed?reportId=2e5b63a0-5664-4674-8f83-269b22ce53ee&autoAuth=true&ctid=026e0585-0f6d-4eb2-ba93-8c4a4d4883c4" frameborder="0" allowFullScreen="true"></iframe> -->
            <PowerBIQnaEmbed style="width:100vw; height:90vh;" :embedConfig="embedConfig" :eventHandlers="eventHandlersMap" ref="qnaEmbed"></PowerBIQnaEmbed>
            <v-btn @click="getQuestion">Get Question</v-btn>
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
    // import { saveAs } from 'file-saver';

    export default {
        name: 'PowerBI',
        components: {
            PowerBIQnaEmbed
        },
        data() {
            return {
                embedConfig: {
                    type: "report",
                    id: "2e5b63a0-5664-4674-8f83-269b22ce53ee",
                    embedUrl: "https://app.powerbi.com/reportEmbed?reportId=2e5b63a0-5664-4674-8f83-269b22ce53ee&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly9XQUJJLVVTLU5PUlRILUNFTlRSQUwtcmVkaXJlY3QuYW5hbHlzaXMud2luZG93cy5uZXQiLCJlbWJlZEZlYXR1cmVzIjp7InVzYWdlTWV0cmljc1ZOZXh0Ijp0cnVlfX0%3d",
                    accessToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJodHRwczovL2FuYWx5c2lzLndpbmRvd3MubmV0L3Bvd2VyYmkvYXBpIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMDI2ZTA1ODUtMGY2ZC00ZWIyLWJhOTMtOGM0YTRkNDg4M2M0LyIsImlhdCI6MTY5NTg4NTgxNCwibmJmIjoxNjk1ODg1ODE0LCJleHAiOjE2OTU4OTEzNjYsImFjY3QiOjAsImFjciI6IjEiLCJhaW8iOiJBVlFBcS84VUFBQUFGYVkyTlR3V1dwOHkxWEFtWGJENm5rWnRKT1JCODZYQm5NeW5Pa0ZiekxwQ0YxUVlPOG1leEZNb2NjV25WaHRMQjRtRHZ4eHJkbVBKQzR5cUlFRSs4WHdwS3JCaTlLeWVueE9jaXNLUFBWOD0iLCJhbXIiOlsicHdkIiwicnNhIiwibWZhIl0sImFwcGlkIjoiODcxYzAxMGYtNWU2MS00ZmIxLTgzYWMtOTg2MTBhN2U5MTEwIiwiYXBwaWRhY3IiOiIwIiwiZGV2aWNlaWQiOiI1N2Y1MzlkMC1jYWZkLTRjNmEtYTFiOC1mYmQ1MGFjYTk5ZDAiLCJmYW1pbHlfbmFtZSI6IktoYW4iLCJnaXZlbl9uYW1lIjoiTXVoYW1tYWQgQmlsYWwiLCJpcGFkZHIiOiIxMTcuMjAuMTYuMjAiLCJuYW1lIjoiTXVoYW1tYWQgQmlsYWwgS2hhbiIsIm9pZCI6IjIyMjBiYWE5LTlkZTctNGUxZC04ZWJhLWYzZDZlNzM0MDExZCIsInB1aWQiOiIxMDAzMjAwMEYwNzZBNTY4IiwicmgiOiIwLkFYY0FoUVZ1QW0wUHNrNjZrNHhLVFVpRHhBa0FBQUFBQUFBQXdBQUFBQUFBQUFCM0FKby4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzaWduaW5fc3RhdGUiOlsiaW5rbm93bm50d2siLCJrbXNpIl0sInN1YiI6Im4wWjFzM0VfY0Y0TjZTZUpkdUNIMVdtS2lHN2Z5MWlFaVlYWml2OThlc2ciLCJ0aWQiOiIwMjZlMDU4NS0wZjZkLTRlYjItYmE5My04YzRhNGQ0ODgzYzQiLCJ1bmlxdWVfbmFtZSI6ImJpbGFsLmtoYW5AcW9yZGF0YS5jb20iLCJ1cG4iOiJiaWxhbC5raGFuQHFvcmRhdGEuY29tIiwidXRpIjoiR0dGLWNjTVlsRUtPNTllZE5RSldBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il19.dVWZ4cKYw89yg_kyLWf8FzK0PwGrE4BosW8x4w2HY1Z_WseeeOChz3Mhs96IzoEOBycoJIzzWjuryKgB6b80BlQcW0Gn85de-Qxhvy1k_FiNRumuwwIias4oUQucYzgNiwHWJBnJoRX4YAodKEiNFgWT8z1S1rBl4gSRM2tKE4WEVxI42uXj6863MtAnxsxlYJ4xSXK8qloK808_mrZE-pRz7pZUlTuP7S09E-TY65DsZ7-eXYryeNGAL0OV9u3brajj74y717GRkbqyJvbUP9xqN0WX0ehjnZeKUjpMXjlgEl5TwHTeLBGOP7uZ3slTPLziILpqYkcfe18UpjlmWw",
                    datasetIds: ["cb638450-1d08-4124-9d71-b6068ad37f54"],
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
                        background: models.BackgroundType.Transparent,
                        filterPaneEnabled: false,
                        navContentPaneEnabled: false,
                        visualRenderedEvents: true // Because visuals might render due to user interactions, it's recommended that this event only be turned on when needed.
                    }
                },
                eventHandlersMap: new Map([
                    ['loaded', () => console.log('Report has loaded')],
                    ['rendered', () => console.log('Report has rendered')],
                    ['error', () => console.log('Report has rendered')],
                    // ['visualClicked', () => console.log('visual clicked')],
                    // ['pageChanged', () => console.log('Page change')],
                    ['visualRendered', async () => {
                        let qnaContainer = this.$refs.qnaEmbed
                        this.report = await qnaContainer.getQna()
                        let activePage = await this.report.getActivePage();
                        let visuals = await activePage.getVisuals();
                        console.log(visuals)
                    }]
                ]),
                drawer: false,
                snackMessage: '',
                snackColor: '',
                snackExecution: false,
                isLogout: false,
                report: null,
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
            setReportObj(value) {
                console.log("Report value ", value)
                this.report = value;
            },
            async onVisualRendered() {
                let qnaContainer = this.$refs.getQna
                this.report = await qnaContainer.getQna()
                let activePage = await this.report.getActivePage();
                let visuals = await activePage.getVisuals();
                
                // Export each visual as an image.
                for (let visual of visuals) {
                    let result =  visual.exportData(models.ExportDataType.Image);
                    let imageUrl = result.exportedFile.url;
                    console.log(imageUrl);
                    let fileName = 'visual_' + visual.name + '.png';
                    saveAs(imageUrl, fileName);
                }
            },
            getQuestion() {
                const qnaEmbed = this.$refs.qnaEmbed;
                qnaEmbed.getQuestion().then(question => {
                console.log(question);
                });
            }
        }
    }
</script>