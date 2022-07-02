<template>
    <div id="app">
        <v-app id="inspire">
            <v-navigation-drawer v-model="drawer" app>
                <v-container>
                    <v-row justify="center" align="center">
                        <v-col>
                            <ul>
                                <p style="font-size: x-large">Quick Access</p>
                                <li><a href="#home">Home</a></li>
                                <li><a href="#kri_details">KRI Details</a></li>
                                <li><a href="#kri_parameters">KRI Parameters</a></li>
                                <li><a href="#lookback_configuration">Lookback Configuration</a></li>
                                <li><a href="#ValidationErrors">Vaidation Errors</a></li>
                                <li><a href="#time_frame">Time Frames</a></li>
                                <li><a href="#RiskyTransactions">Risky Transactions</a></li>
                                <li><a href="#WarningsTable">Warnings</a></li>
                            </ul>
                        </v-col>
                    </v-row>
                </v-container>
            </v-navigation-drawer>

            <v-app-bar app>
                <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
                <v-toolbar-title>Compliance Monitoring Logs</v-toolbar-title>
            </v-app-bar>

            <v-main>
                <v-container>
                    <v-row>
                        <v-col>
                            <v-row>
                                <v-col cols="4"><img src=".\assets\Pandas_Black.png" class="logo newline" id="home" /></v-col>
                                <v-col v-if="tableLoad.every (value => value === false)">
                                    <img :src="require('./assets/' + gif_path)" class="logo newline" alt="Status image" />
                                    <div>{{ status_message }}</div>
                                </v-col>
                            </v-row>
                        </v-col>
                        <v-col>
                            <v-col class="newline"><multiselect v-model="server" :options="servers" placeholder="Select Server" @input="getDatabases"></multiselect></v-col>
                            <v-col class="newline"><multiselect v-model="database" :options="databases" placeholder="Select Database" @input="jobName"></multiselect></v-col>
                            <v-snackbar v-model="selectSnack" :timeout="5000" :color="snackColor">
                                {{ snackText }}
                                <template v-slot:action="{ attrs }">
                                    <v-btn v-bind="attrs" text @click="selectSnack = false"> Close </v-btn>
                                </template>
                            </v-snackbar>
                            <v-col class="newline">
                                <v-row>
                                    <v-col>
                                        <v-btn class="ma-3" :loading="tableLoadCount != 7" :disabled="tableLoadCount != 7" color="success" @click="fetchData" elevation="5">
                                            Fetch Data
                                            <!--<template v-slot:"tableLoad.every (value => value === true)">
                                                <span>Loading...</span>
                                            </template>-->
                                        </v-btn>
                                    </v-col>
                                    <v-col>
                                        <v-btn class="ma-3" :loading="commit" :disabled="commit" color="primary" @click="commitChanges" elevation="5">
                                            Commit Change
                                            <template v-slot:commit>
                                                <span>Updating...</span>
                                            </template>
                                        </v-btn>
                                    </v-col>
                                    <v-col>
                                        <v-dialog transition="dialog-top-transition"
                                                  max-width="600">
                                            <template v-slot:activator="{ on, attrs }">
                                                <v-btn color="warning" v-bind="attrs" v-on="on" elevation="5" style="margin-top:12px;" :loading="job_execution" :disabled="job_execution">Execute Job</v-btn>
                                            </template>
                                            <template v-slot:default="dialog">
                                                <v-card>
                                                    <v-toolbar color="warning" dark>Do you want to execute?</v-toolbar>
                                                    <v-card-text>
                                                        <h2 class="newline">{{ job_name }}</h2>
                                                        <v-row>
                                                            <v-col class="d-flex newline"
                                                                   cols="12"
                                                                   sm="6">
                                                                <v-select :items="job_steps" label="Starting Step" v-model="start_step"></v-select>
                                                            </v-col>
                                                        </v-row>
                                                    </v-card-text>
                                                    <v-card-actions class="justify-end">
                                                        <v-btn text @click="dialog.value = false">I change my mind</v-btn>
                                                        <v-btn text @click="executeJob(); dialog.value = false;">Go for it!</v-btn>
                                                    </v-card-actions>
                                                </v-card>
                                            </template>
                                        </v-dialog>
                                        <v-snackbar v-model="executionSnack" :timeout="5000" :color="snackColor">
                                            {{ snackText }}
                                            <template v-slot:action="{ attrs }">
                                                <v-btn v-bind="attrs" text @click="executionSnack = false"> Close </v-btn>
                                            </template>
                                        </v-snackbar>
                                    </v-col>
                                </v-row>
                            </v-col>
                        </v-col>
                    </v-row>
                </v-container>
                <!-- KRI Details Table -->
                <v-container>
                    <v-row>
                        <v-col>
                            <div id="kri_details">
                                <v-data-table :headers="headers_kri" :items="datum_kri" :search="search" multi-sort :loading="tableLoad[0]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                    <template v-slot:top>
                                        <v-toolbar flat>
                                            <v-toolbar-title class="tableHeader"> KRI Details </v-toolbar-title>
                                            <v-divider class="mx-4" inset vertical></v-divider>
                                            <v-spacer></v-spacer>
                                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                        </v-toolbar>
                                    </template>
                                    <template v-slot:item.kri_name="props">
                                        <v-edit-dialog :return-value.sync="props.item.kri_name" @save="save(props.item.ID, props.item.kri_name, 'kri_name', 'kri_details')" @cancel="cancel" @open="open" persistent>
                                            {{ props.item.kri_name }}
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.kri_name" :rules="[max25chars]" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                    <template v-slot:item.is_active="props">
                                        <v-edit-dialog :return-value.sync="props.item.is_active" @save="save(props.item.ID, props.item.is_active, 'is_active', 'kri_details')" @cancel="cancel" @open="open" persistent>
                                            <v-chip :color="getColor(props.item.is_active)" dark>
                                                {{ props.item.is_active }}
                                            </v-chip>
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.is_active" :rules="[isBinary]" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                    <template v-slot:item.Weightage="props">
                                        <v-edit-dialog :return-value.sync="props.item.Weightage" @save="save(props.item.ID, props.item.Weightage, 'Weightage', 'kri_details')" @cancel="cancel" @open="open" persistent>
                                            {{ props.item.Weightage }}
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.Weightage" :rules="[max25chars]" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                    <template v-slot:item.YTD="props">
                                        <v-edit-dialog :return-value.sync="props.item.YTD" @save="save(props.item.ID, props.item.YTD, 'YTD', 'kri_details')" @cancel="cancel" @open="open" persistent>
                                            {{ props.item.YTD }}
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.YTD" :rules="[max25chars]" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                    <template v-slot:item.date_field="props">
                                        <v-edit-dialog :return-value.sync="props.item.date_field" @save="save(props.item.ID, props.item.date_field, 'date_field', 'kri_details')" @cancel="cancel" @open="open" persistent>
                                            {{ props.item.date_field }}
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.date_field" :rules="[max25chars]" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                    <template v-slot:item.template_agg_dimension="props">
                                        <v-edit-dialog :return-value.sync="props.item.template_agg_dimension" @save="save(props.item.ID, props.item.template_agg_dimension, 'template_agg_dimension', 'kri_details')" @cancel="cancel" @open="open" persistent>
                                            {{ props.item.template_agg_dimension }}
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.template_agg_dimension" :rules="[max25chars]" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                    <template v-slot:item.template_agg_column="props">
                                        <v-edit-dialog :return-value.sync="props.item.template_agg_column" @save="save(props.item.ID, props.item.template_agg_column, 'template_agg_column', 'kri_details')" @cancel="cancel" @open="open" persistent>
                                            {{ props.item.template_agg_column }}
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.template_agg_column" :rules="[max25chars]" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                </v-data-table>

                                <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                                    {{ snackText }}

                                    <template v-slot:action="{ attrs }">
                                        <v-btn v-bind="attrs" text @click="snack = false"> Close </v-btn>
                                    </template>
                                </v-snackbar>
                            </div>
                        </v-col>
                    </v-row>
                </v-container>
                <v-container>
                    <v-row>
                        <v-col>
                            <!-- KRI Parameters -->
                            <div id="kri_parameters">
                                <v-data-table :headers="headers_params" :items="datum_params" :search="search" multi-sort :loading="tableLoad[1]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                    <template v-slot:top>
                                        <v-toolbar flat>
                                            <v-toolbar-title class="tableHeader"> KRI Parameters </v-toolbar-title>
                                            <v-divider class="mx-4" inset vertical></v-divider>
                                            <!--<v-btn color="primary" class="mb-2" v-bind="attrs" v-on="on" elevation="5" @click="commitChanges('kri_parameters')"> Commit Changes </v-btn>-->
                                            <v-spacer></v-spacer>
                                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                        </v-toolbar>
                                    </template>
                                    <template v-slot:item.Param_value="props">
                                        <v-edit-dialog :return-value.sync="props.item.Param_value" @save="save(props.item.ID, props.item.Param_value, 'Param_value', 'kri_parameters')" @cancel="cancel" @open="open" persistent>
                                            {{ props.item.Param_value }}
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.Param_value" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                </v-data-table>
                                <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                                    {{ snackText }}
                                    <template v-slot:action="{ attrs }">
                                        <v-btn v-bind="attrs" text @click="snack = false"> Close </v-btn>
                                    </template>
                                </v-snackbar>
                            </div>
                        </v-col>
                        <v-col>
                            <!-- Risk Algo Parameters Table -->
                            <div id="RiskAlgoParamaeters">
                                <v-data-table :headers="headers_algo_params" :items="datum_algo_params" :search="search" multi-sort :loading="tableLoad[2]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                    <template v-slot:top>
                                        <v-toolbar flat>
                                            <v-toolbar-title class="tableHeader"> Risk Algo. Parameters </v-toolbar-title>
                                            <v-divider class="mx-4" inset vertical></v-divider>
                                            <v-spacer></v-spacer>
                                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                        </v-toolbar>
                                    </template>
                                    <template v-slot:item.isMandatory="props">
                                        <v-edit-dialog :return-value.sync="props.item.isMandatory" @save="save(props.item.ID, props.item.isMandatory, 'isMandatory', 'RiskAlgoParameters')" @cancel="cancel" @open="open" persistent>
                                            <v-chip :color="getColor(props.item.isMandatory)" dark>
                                                {{ props.item.isMandatory }}
                                            </v-chip>
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.isMandatory" :rules="[isBinary]" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                </v-data-table>

                                <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                                    {{ snackText }}
                                    <template v-slot:action="{ attrs }">
                                        <v-btn v-bind="attrs" text @click="snack = false"> Close </v-btn>
                                    </template>
                                </v-snackbar>
                            </div>
                            <div id="lookback_configuration">
                                <v-data-table :headers="headers_lookback" :items="datum_lookback" :search="search" multi-sort :loading="tableLoad[7]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                    <template v-slot:top>
                                        <v-toolbar flat>
                                            <v-toolbar-title class="tableHeader"> Lookback Configuration </v-toolbar-title>
                                            <v-divider class="mx-4" inset vertical></v-divider>
                                            <v-spacer></v-spacer>
                                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                        </v-toolbar>
                                    </template>
                                    <template v-slot:item.lookback_period="props">
                                        <v-edit-dialog :return-value.sync="props.item.lookback_period" @save="save(props.item.id, props.item.lookback_period, 'lookback_period', 'lookback_configuration')" @cancel="cancel" @open="open" persistent>
                                            <v-chip :color="getColor(props.item.lookback_period)" dark>
                                                {{ props.item.lookback_period }}
                                            </v-chip>
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.lookback_period" :rules="[maxTimeFrame]" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                </v-data-table>

                                <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                                    {{ snackText }}
                                    <template v-slot:action="{ attrs }">
                                        <v-btn v-bind="attrs" text @click="snack = false"> Close </v-btn>
                                    </template>
                                </v-snackbar>
                            </div>
                        </v-col>
                    </v-row>
                </v-container>
                <v-container>
                    <v-row>
                        <v-col>
                            <!-- Validation Errors Table -->
                            <div id="ValidationErrors">
                                <v-data-table :headers="headers_errors" :items="datum_errors" :search="search" multi-sort :loading="tableLoad[3]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                    <template v-slot:top>
                                        <v-toolbar flat>
                                            <v-toolbar-title class="tableHeader"> Validation Errors </v-toolbar-title>
                                            <v-divider class="mx-4" inset vertical></v-divider>
                                            <!--<v-btn color="primary" class="mb-2" v-bind="attrs" v-on="on" elevation="5" @click="commitChanges('RiskAlgoParameters')"> Commit Changes </v-btn>-->
                                            <v-spacer></v-spacer>
                                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                        </v-toolbar>
                                    </template>
                                </v-data-table>

                                <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                                    {{ snackText }}
                                    <template v-slot:action="{ attrs }">
                                        <v-btn v-bind="attrs" text @click="snack = false"> Close </v-btn>
                                    </template>
                                </v-snackbar>
                            </div>
                        </v-col>
                        <v-col>
                            <!-- Time Frames Table -->
                            <div id="time_frame">
                                <v-data-table :headers="headers_time_frame" :items="datum_time_frame" :search="search" multi-sort :loading="tableLoad[4]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                    <template v-slot:top>
                                        <v-toolbar flat>
                                            <v-toolbar-title class="tableHeader"> Time Frames </v-toolbar-title>
                                            <v-divider class="mx-4" inset vertical></v-divider>
                                            <v-spacer></v-spacer>
                                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                        </v-toolbar>
                                    </template>
                                    <template v-slot:item.timeSpan="props">
                                        <v-edit-dialog :return-value.sync="props.item.timeSpan" @save="save(props.item.id, props.item.timeSpan, 'timeSpan', 'time_frame')" @cancel="cancel" @open="open" persistent>
                                            {{ props.item.timeSpan }}
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.timeSpan" :rules="[maxTimeFrame]" label="Edit" single-line></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                    <template v-slot:item.isActive="props">
                                        <v-edit-dialog :return-value.sync="props.item.isActive" @save="save(props.item.id, props.item.isActive, 'isActive', 'time_frame')" @cancel="cancel" @open="open" persistent>
                                            <v-chip :color="getColor(props.item.isActive)" dark>
                                                {{ props.item.isActive }}
                                            </v-chip>
                                            <template v-slot:input>
                                                <v-text-field v-model="props.item.isActive" :rules="[isBinary]" label="Edit" single-line counter></v-text-field>
                                            </template>
                                        </v-edit-dialog>
                                    </template>
                                </v-data-table>

                                <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                                    {{ snackText }}
                                    <template v-slot:action="{ attrs }">
                                        <v-btn v-bind="attrs" text @click="snack = false"> Close </v-btn>
                                    </template>
                                </v-snackbar>
                            </div>
                        </v-col>
                    </v-row>
                </v-container>
                <v-container>
                    <v-row>
                        <v-col>
                            <!-- Risky Transactions Table -->
                            <div id="RiskyTransactions">
                                <v-data-table :headers="headers_transactions" :items="datum_transactions" :search="search" multi-sort :loading="tableLoad[5]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                    <template v-slot:top>
                                        <v-toolbar flat>
                                            <v-toolbar-title class="tableHeader"> Risky Transactions </v-toolbar-title>
                                            <v-divider class="mx-4" inset vertical></v-divider>
                                            <v-spacer></v-spacer>
                                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                        </v-toolbar>
                                    </template>
                                    <template v-slot:item.RiskScore="props">
                                        <v-chip :color="getRiskColor(props.item.RiskScore)" dark>
                                            {{ props.item.RiskScore }}
                                        </v-chip>
                                    </template>
                                </v-data-table>

                                <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                                    {{ snackText }}

                                    <template v-slot:action="{ attrs }">
                                        <v-btn v-bind="attrs" text @click="snack = false"> Close </v-btn>
                                    </template>
                                </v-snackbar>
                            </div>
                        </v-col>
                    </v-row>
                </v-container>
                <v-container>
                    <v-row>
                        <v-col>
                            <!-- Warnings Table -->
                            <div id="WarningsTable">
                                <v-data-table :headers="headers_warnings" :items="datum_warnings" :search="search" multi-sort :loading="tableLoad[6]" loading-text="Fetching data... Please wait" class="elevation-5 newline" :items-per-page="5">
                                    <template v-slot:top>
                                        <v-toolbar flat>
                                            <v-toolbar-title class="tableHeader"> Warnings </v-toolbar-title>
                                            <v-divider class="mx-4" inset vertical></v-divider>
                                            <v-spacer></v-spacer>
                                            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                        </v-toolbar>
                                    </template>
                                    <template v-slot:item.IsCritical="props">
                                        <v-chip :color="getColor(props.item.IsCritical)" dark>
                                            {{ props.item.IsCritical }}
                                        </v-chip>
                                    </template>
                                </v-data-table>

                                <v-snackbar v-model="snack" :timeout="3000" :color="snackColor">
                                    {{ snackText }}

                                    <template v-slot:action="{ attrs }">
                                        <v-btn v-bind="attrs" text @click="snack = false"> Close </v-btn>
                                    </template>
                                </v-snackbar>
                            </div>
                        </v-col>
                    </v-row>
                </v-container>
            </v-main>
        </v-app>
    </div>
</template>

<script>
    import Multiselect from 'vue-multiselect';
    import 'vue-multiselect/dist/vue-multiselect.min.css';
    import axios from 'axios';
    import 'victormono';

    export default {
        name: 'app',
        components: {
            Multiselect
        },
        data() {
            return {
                num: null,
                backend: "http://localhost:5555",
                tableLoadCount: 7,
                status_message: null,
                job_name: '',
                job_steps: [],
                start_step: null,
                gif_path: 'blank.png',
                search: '',
                database: null,
                server: null,
                servers: ['US-BCKND', 'QA-US-BCKND'],
                databases: [],
                tableLoad: [false, false, false, false, false, false, false, false],
                commit: false,
                job_execution: false,
                job_status: null,
                drawer: false,
                snack: false,
                selectSnack: false,
                executionSnack: false,
                snackColor: '',
                snackText: '',
                max25chars: v => v.length <= 25 || 'Input too long!',
                isBinary: v => v >= 0 && v <= 1 || 'Value must be binary',
                maxTimeFrame: v => v >= 1 && v <= 12 || 'Last I checked, there are 12 months in a year!',
                pagination: {},
                headers_kri: [
                    { text: 'ID', value: 'ID' },
                    { text: 'KRI Name', value: 'kri_name' },
                    { text: 'Active', value: 'is_active' },
                    { text: 'Time Frame', value: 'time_frame' },
                    { text: 'Weightage', value: 'Weightage' },
                    { text: 'YTD', value: 'YTD' },
                    { text: 'Date Type', value: 'data_type' },
                    { text: 'Date Field', value: 'date_field' },
                    { text: 'Start Date', value: 'date_from' },
                    { text: 'End Date', value: 'date_to' },
                    { text: 'Agg. Dim.', value: 'template_agg_dimension' },
                    { text: 'Agg. Col.', value: 'template_agg_column' }
                ],
                headers_algo_params: [
                    { text: 'ID', value: 'ID' },
                    { text: 'Algo. ID', value: 'RiskAlgoID' },
                    { text: 'Param. Name', value: 'Param_name' },
                    { text: 'Param. Type', value: 'Param_type' },
                    { text: 'Mandatory', value: 'isMandatory' },
                ],
                headers_params: [
                    { text: 'ID', value: 'ID' },
                    { text: 'KRI ID', value: 'kri_id' },
                    { text: 'Param. ID', value: 'param_id' },
                    { text: 'Param. Value', value: 'Param_value' }
                ],
                headers_errors: [
                    { text: 'ID', value: 'ID' },
                    { text: 'Year', value: 'Year' },
                    { text: 'Data Type', value: 'DataType' },
                    { text: 'Version Col. ID', value: 'VersionColID' },
                    { text: 'Rule ID', value: 'RuleID' },
                    { text: 'Transaction ID', value: 'TransactionID' },
                    { text: 'LZ Record ID', value: 'LZRecordID' }
                ],
                headers_time_frame: [
                    { text: 'ID', value: 'id' },
                    { text: 'Time Span', value: 'timeSpan' },
                    { text: 'Active', value: 'isActive' }
                ],
                headers_transactions: [
                    { text: 'ID', value: 'ID' },
                    { text: 'Data Type', value: 'DataType' },
                    { text: 'KRI ID', value: 'KRIID' },
                    { text: 'Risk Algo. ID', value: 'RiskAlgoID' },
                    { text: 'Agg. Dimension', value: 'TemplateAggDimension' },
                    { text: 'Agg. Dimension Value', value: 'TemplateAggDimensionValue' },
                    { text: 'Agg. Column', value: 'TemplateAggColumn' },
                    { text: 'Agg. Column Value', value: 'TemplateAggColumnValue' },
                    { text: 'Risk Score', value: 'RiskScore' },
                    { text: 'Weight Score', value: 'WeightScore' },
                    { text: 'Start Date', value: 'DateFrom' },
                    { text: 'End Date', value: 'DateTo' }
                ],
                headers_warnings: [
                    { text: 'ID', value: 'Id' },
                    { text: 'KRI ID', value: 'KRIID' },
                    { text: 'Message', value: 'Message' },
                    { text: 'Method', value: 'Method' },
                    { text: 'Error Column', value: 'ErrorColumn' },
                    { text: 'Error Table', value: 'ErrorTable' },
                    { text: 'Line Number', value: 'LineNumber' },
                    { text: 'Critical', value: 'IsCritical' },
                    { text: 'Timestamp', value: 'Timestamp' }
                ],
                headers_lookback: [
                    { text: 'ID', value: 'id' },
                    { text: 'KRI ID', value: 'kriid' },
                    { text: 'KRI Name', value: 'kriname' },
                    { text: 'Lookback Period', value: 'lookback_period' },
                ],
                datum_kri: [],
                datum_params: [],
                datum_algo_params: [],
                datum_errors: [],
                datum_time_frame: [],
                datum_transactions: [],
                datum_warnings: [],
                datum_lookback: [],
                queries: []
            }
        },
        methods: {
            getDatabases() {
                axios.get(this.backend + '/getDatabaseName?server=' + this.server).then(response => {
                    this.databases = Object.values(JSON.parse(response.data));
                }).catch(err => {
                    console.log(err);
                });
            },
            jobName() {
                if (this.database == 'ComplianceMonitoring') this.job_name = 'ComplianceMonitoringDemo';
                else this.job_name = this.database.replaceAll('_', '');

                axios.get(this.backend + '/jobSteps?server=' + this.server + '&job_name=' + this.job_name).then(response => {
                    this.job_steps = Object.values(JSON.parse(response.data));
                }).catch(err => {
                    console.log(err);
                });
            },
            executeJob() {
                this.job_execution = true;
                let updates = {
                    server: this.server,
                    job_name: this.job_name,
                    start_step: this.start_step
                };
                axios.post(this.backend + '/jobSteps', updates).then(response => {
                    this.job_execution = false;
                    try {
                        this.job_status = Object.values(JSON.parse(response.data));
                        if (this.job_status[0] == 1) {
                            this.snackText = 'Job Execution in Progress';
                            this.snackColor = 'default';
                            this.executionSnack = true;
                            console.log(this.job_status[0], "Job execution in progress");
                        }
                        else {
                            this.snackText = 'Error in Execution';
                            this.snackColor = 'error';
                            this.executionSnack = true;
                            console.log(this.job_status[0], "Error in execution");
                        }
                    } catch (err) {
                        this.snackText = 'Error in RPC';
                        this.snackColor = 'error';
                        this.executionSnack = true;
                        console.log(this.job_status[0], "Error in execution");
                    }
                });
            },
            save(id, newValue, column, table) {
                this.snack = true
                this.snackColor = 'success'
                this.snackText = 'Data saved'
                //if (column == 'is_active' && (newValue != 0 && newValue != 1)) newValue = 0
                this.queries.push('UPDATE ' + table + ' SET ' + column + ' = ' + newValue + ' WHERE ID = ' + id)
                console.log(this.queries)
            },
            cancel() {
                this.snack = true
                this.snackColor = 'error'
                this.snackText = 'Canceled'
            },
            open() {
                this.snack = true
                this.snackColor = 'info'
                this.snackText = 'Dialog opened'
            },
            getColor(is_active) {
                if (is_active == 1) return 'green'
                else if (is_active == 0) return 'orange'
                else return 'red'
            },
            getRiskColor(risk) {
                if (risk <= 5) return 'green'
                else if (risk > 5 && risk < 10) return 'orange'
                else return 'red'
            },
            commitChanges() {
                this.commit = true;
                let updates = {
                    server: this.server,
                    db: this.database,
                    queries: this.queries
                };
                axios.post(this.backend + '/getData', updates).then(response => {
                    this.commit = false;
                    if (response.data == 400) {
                        this.snackText = 'Could not commit changes';
                        this.snackColor = 'error';
                        this.executionSnack = true;
                    }
                    else {
                        this.snackText = 'Changes commited';
                        this.snackColor = 'success';
                        this.executionSnack = true;
                    }
                    console.log(response.data);
                });
            },
            verifyStatus() {
                if (this.datum_transactions.length == 0) {
                    this.status_message = 'Risky transactions is empty';
                    this.num = Math.floor(Math.random() * 2);
                    if (this.num == 1) this.gif_path = "crashed.gif";
                    else this.gif_path = "elmo_fire.gif";
                }
                else if (this.datum_warnings.length == 0 && this.datum_errors.length == 0) {
                    this.status_message = 'All good :)';
                    this.num = Math.floor(Math.random() * 5);
                    switch (this.num) {
                        case 0:
                            this.gif_path = "all_good_crazy_frog.gif";
                            break;
                        case 1:
                            this.gif_path = "all_good_maverick.gif";
                            break;
                        case 2:
                            this.gif_path = "all_good_aeroplane.gif";
                            break;
                        case 3:
                            this.gif_path = "having_trouble_maverick.gif";
                            break;
                        case 4:
                            this.gif_path = "thumbs_up_kitty.png";
                            break;
                    }
                    
                }
                else if (this.datum_warnings.length == 0 || this.datum_errors.length == 0) {
                    this.status_message = 'All good! See some warnings';
                    this.num = Math.floor(Math.random() * 5);
                    switch (this.num) {
                        case 0:
                            this.gif_path = "all_good_crazy_frog.gif";
                            break;
                        case 1:
                            this.gif_path = "all_good_maverick.gif";
                            break;
                        case 2:
                            this.gif_path = "all_good_aeroplane.gif";
                            break;
                        case 3:
                            this.gif_path = "having_trouble_maverick.gif";
                            break;
                        case 4:
                            this.gif_path = "thumbs_up_kitty.png";
                            break;
                    }
                }
                else {
                    this.staus_message = 'Job crash :(';
                    this.num = Math.floor(Math.random() * 2);
                    if (this.num == 1) this.gif_path = "crashed.gif";
                    else this.gif_path = "elmo_fire.gif";
                }
            },
            async fetchData() {
                this.tableLoadCount = -1;
                if (this.database === null || this.server === null) {
                    this.selectSnack = true
                    this.snackColor = 'error'
                    this.snackText = 'Please make sure server and database is selected'
                }
                else {
                    this.tableLoad.fill(true);
                    // Fetch kri_details
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=kri_details&server=' + this.server).then(response => {
                        this.datum_kri = Object.values(JSON.parse(response.data));
                        this.tableLoad[0] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch kri_parameters
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=kri_parameters&server=' + this.server).then(response => {
                        this.datum_params = Object.values(JSON.parse(response.data));
                        this.tableLoad[1] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch RiskAlgoParameters
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=RiskAlgoParameters&server=' + this.server).then(response => {
                        this.datum_algo_params = Object.values(JSON.parse(response.data));
                        this.tableLoad[2] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch ValidationErrors
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=ValidationErrors&server=' + this.server).then(response => {
                        this.datum_errors = Object.values(JSON.parse(response.data));
                        this.tableLoad[3] = false;
                        this.tableLoadCount++;
                        this.verifyStatus();
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch time_frames
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=time_frames&server=' + this.server).then(response => {
                        this.datum_time_frame = Object.values(JSON.parse(response.data));
                        this.tableLoad[4] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch RiskyTransactions
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=RiskyTransactions&server=' + this.server).then(response => {
                        this.datum_transactions = Object.values(JSON.parse(response.data));
                        this.tableLoad[5] = false;
                        this.tableLoadCount++;
                        this.verifyStatus();
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch WarningTable
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=WarningTable&server=' + this.server).then(response => {
                        this.datum_warnings = Object.values(JSON.parse(response.data));
                        this.tableLoad[6] = false;
                        this.tableLoadCount++;
                        this.verifyStatus();
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch Lookback Configuration
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=lookback_configuration&server=' + this.server).then(response => {
                        this.datum_lookback = Object.values(JSON.parse(response.data));
                        this.tableLoad[7] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                }
            }
        }
    };
</script>

<style>
    div {
        font-family: 'Victor Mono'
    }

    .logo {
        max-height: 75%;
        max-width: 75%;
    }

    .newline {
        margin-top: 20px;
    }

    .custom-loader {
        animation: loader 1s infinite;
        display: flex;
    }

    .tableHeader {
        font-style: oblique;
    }

    html {
        scroll-behavior: smooth;
    }
</style>