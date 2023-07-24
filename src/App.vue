<template>
    <div id="app">
        <div v-if="!is_authenticated">
            <v-app>
                <v-container>
                    <v-row style="margin-top:15%;">
                        <v-col></v-col>
                        <v-col>
                            <v-row>
                                <v-col cols="4"><img src=".\assets\Pandas_Black.png" class="logo newline"/></v-col>
                            </v-row>
                            <v-form ref="form"
                                    v-model="valid"
                                    lazy-validation>
                                <v-text-field v-model="password"
                                              :counter="30"
                                              :rules="passwordRules"
                                              label="Password"
                                              :append-icon="value ? 'mdi-eye' : 'mdi-eye-off'"
                                              @click:append="() => (value = !value)"
                                              :type="value ? 'password' : 'text'"
                                              required></v-text-field>

                                <v-text-field v-model="email"
                                              :rules="emailRules"
                                              label="E-mail"
                                              required></v-text-field>

                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn :disabled="!valid"
                                               color="primary"
                                               v-bind="attrs"
                                               v-on="on"
                                               @click="validate(false)">
                                            Login
                                        </v-btn>
                                    </template>
                                    <span>With great powers, comes great responsibility</span>
                                </v-tooltip>

                                <v-dialog transition="dialog-top-transition"
                                          max-width="600">
                                    <template v-slot:activator="{ on, attrs }">
                                        <!--<v-btn v-bind="attrs" v-on="on" elevation="5">New to C</v-btn>-->
                                        <a v-bind="attrs" v-on="on" style="font-size: small; margin-left: 10%;">New to Compliance Monitoring?</a>
                                    </template>
                                    <template v-slot:default="dialog">
                                        <v-card>
                                            <v-toolbar color="#8B008B" dark>Create your ID</v-toolbar>
                                            <v-card-text>
                                                <h2 class="newline">Welcome to the team!</h2>
                                                <v-row>
                                                    <v-form ref="form"
                                                            v-model="new_valid"
                                                            lazy-validation
                                                            class="newline"
                                                            style="margin-left:2%;">
                                                        <v-text-field v-model="password"
                                                                      :counter="30"
                                                                      :rules="passwordRules"
                                                                      label="Password"
                                                                      :append-icon="value ? 'mdi-eye' : 'mdi-eye-off'"
                                                                      @click:append="() => (value = !value)"
                                                                      :type="value ? 'password' : 'text'"
                                                                      required
                                                                      >
                                                        </v-text-field>

                                                        <v-text-field v-model="email"
                                                                      :rules="emailRules"
                                                                      label="E-mail"
                                                                      required>
                                                        </v-text-field>
                                                    </v-form>
                                                </v-row>
                                            </v-card-text>
                                            <v-card-actions class="justify-end">
                                                <v-btn text @click="dialog.value = false">Maybe Later</v-btn>
                                                <v-btn text @click="validate(true); dialog.value = false;" :disabled="!new_valid">Sign me up!</v-btn>
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
                            </v-form>
                        </v-col>
                        <v-col></v-col>
                    </v-row>
                </v-container>
            </v-app>
        </div>
        <div v-if="is_authenticated">
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
                                    <li><a href="#algo_dictionary">Risk Algo Dictionary</a></li>
                                    <li><a href="#execution_time">Execution Time</a></li>
                                    <li><a href="#risk_audit">Risk Audit Logs</a></li>
                                    <li><a href="#file_specs">File Specs</a></li>
                                    <li><a href="#rule_dictionary">Rule Dictionary</a></li>
                                </ul>
                            </v-col>
                        </v-row>
                    </v-container>
                    <v-container style="margin-top: 70%;">
                        <v-row>
                            <div>
                                <v-tooltip bottom>
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-btn color="error"
                                               v-bind="attrs"
                                               v-on="on"
                                               @click="logout"
                                               style="width: 200%; margin-left: 30%;">
                                            Log Out
                                        </v-btn>
                                    </template>
                                    <span>Come back soon!</span>
                                </v-tooltip>
                            </div>
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
                                <v-row>
                                    <v-col>
                                        <v-btn class="ma-3" :loading="reset_workbench" :disabled="databaseUpdate" color="#8B008B" @click="resetWorkbench" elevation="5" dark>
                                            Reset Workbench
                                            <template v-slot:commit>
                                                Workbench is empty
                                                Exeucte Job to see effects
                                            </template>
                                        </v-btn>
                                    </v-col>
                                    <v-col>
                                        <v-btn class="ma-3" :loading="reset_defer" :disabled="databaseUpdate" color="#8B008B" @click="resetDefer" elevation="5" dark>
                                            Reset Defer List
                                            <template v-slot:commit>
                                                Defer List is empty
                                                Exeucte Job to see effects
                                            </template>
                                        </v-btn>
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
                                            <v-btn class="ma-3" :loading="tableLoadCount !== 12" :disabled="databaseUpdate" color="success" @click="fetchData" elevation="5">
                                                Fetch Data
                                                <!--<template v-slot:"tableLoad.every (value => value === true)">
                                                    <span>Loading...</span>
                                                </template>-->
                                            </v-btn>
                                        </v-col>
                                        <v-col>
                                            <v-btn class="ma-3" :loading="commit" :disabled="databaseUpdate" color="primary" @click="commitChanges" elevation="5">
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
                                                    <v-btn color="warning" v-bind="attrs" v-on="on" elevation="5" style="margin-top:12px;" :loading="job_execution" :disabled="databaseUpdate">Execute Job</v-btn>
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
                                    <v-data-table :headers="headers_kri" :items="datum_kri" :search="search[0]" multi-sort :loading="tableLoad[0]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> KRI Details </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[0]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
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
                                    <v-data-table :headers="headers_params" :items="datum_params" :search="search[1]" multi-sort :loading="tableLoad[1]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> KRI Parameters </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <!--<v-btn color="primary" class="mb-2" v-bind="attrs" v-on="on" elevation="5" @click="commitChanges('kri_parameters')"> Commit Changes </v-btn>-->
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[1]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
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
                                    <v-data-table :headers="headers_algo_params" :items="datum_algo_params" :search="search[2]" multi-sort :loading="tableLoad[2]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> Risk Algo. Parameters </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[2]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
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
                                    <v-data-table :headers="headers_lookback" :items="datum_lookback" :search="search[3]" multi-sort :loading="tableLoad[7]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> Lookback Configuration </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[3]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
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
                                    <v-data-table :headers="headers_errors" :items="datum_errors" :search="search[4]" multi-sort :loading="tableLoad[3]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> Validation Errors </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <!--<v-btn color="primary" class="mb-2" v-bind="attrs" v-on="on" elevation="5" @click="commitChanges('RiskAlgoParameters')"> Commit Changes </v-btn>-->
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[4]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
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
                                    <v-data-table :headers="headers_time_frame" :items="datum_time_frame" :search="search[5]" multi-sort :loading="tableLoad[4]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> Time Frames </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[5]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                            </v-toolbar>
                                        </template>
                                        <template v-slot:item.timeSpan="props">
                                            <v-edit-dialog :return-value.sync="props.item.timeSpan" @save="save(props.item.id, props.item.timeSpan, 'timeSpan', 'time_frames')" @cancel="cancel" @open="open" persistent>
                                                {{ props.item.timeSpan }}
                                                <template v-slot:input>
                                                    <v-text-field v-model="props.item.timeSpan" :rules="[maxTimeFrame]" label="Edit" single-line></v-text-field>
                                                </template>
                                            </v-edit-dialog>
                                        </template>
                                        <template v-slot:item.isActive="props">
                                            <v-edit-dialog :return-value.sync="props.item.isActive" @save="save(props.item.id, props.item.isActive, 'isActive', 'time_frames')" @cancel="cancel" @open="open" persistent>
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
                                    <v-data-table :headers="headers_transactions" :items="datum_transactions" :search="search[6]" multi-sort :loading="tableLoad[5]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> Risky Transactions </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[6]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
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
                                    <v-data-table :headers="headers_warnings" :items="datum_warnings" :search="search[7]" multi-sort :loading="tableLoad[6]" loading-text="Fetching data... Please wait" class="elevation-5 newline" :items-per-page="5">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> Warnings </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[7]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
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
                    <v-container>
                        <v-row>
                            <v-col>
                                <!-- Risk Algo Dictionary Table -->
                                <div id="algo_dictionary">
                                    <v-data-table :headers="headers_algo_dictionary" :items="datum_algo_dictionary" :search="search[8]" multi-sort :loading="tableLoad[8]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> Risk Algo Dictionary </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[8]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
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
                                <!-- Execution Logs Table -->
                                <div id="execution_time">
                                    <v-data-table :headers="headers_execution_time" :items="datum_execution_time" :search="search[9]" multi-sort :loading="tableLoad[9]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> Execution Time </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[9]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                            </v-toolbar>
                                        </template>
                                        <template v-slot:item.TimeTaken="props">
                                            <v-chip color="black" dark>
                                                {{ props.item.TimeTaken }}
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
                            <v-col>
                                <!-- Risk Audit Logs -->
                                <div id="risk_audit">
                                    <v-data-table :headers="headers_risk_audit" :items="datum_risk_audit" :search="search[12]" multi-sort :loading="tableLoad[12]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> Risk Audit Logs </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[12]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
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
                        </v-row>
                    </v-container>
                    <v-container>
                        <v-row>
                            <v-col>
                                <!-- File Specs -->
                                <div id="file_specs">
                                    <v-data-table :headers="headers_file_specs" :items="datum_file_specs" :search="search[10]" multi-sort :loading="tableLoad[10]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> File Specs </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[10]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                                            </v-toolbar>
                                        </template>
                                        <template v-slot:item.FILE_TPYE="props">
                                            <v-edit-dialog :return-value.sync="props.item.FILE_TPYE" @save="save(props.item.ID, props.item.FILE_TPYE, 'FILE_TPYE', 'File_Specs')" @cancel="cancel" @open="open" persistent>
                                                {{ props.item.FILE_TPYE }}
                                                <template v-slot:input>
                                                    <v-text-field v-model="props.item.FILE_TPYE" label="Edit" single-line counter></v-text-field>
                                                </template>
                                            </v-edit-dialog>
                                        </template>
                                        <template v-slot:item.FILE_TPYE="props">
                                            <v-edit-dialog :return-value.sync="props.item.PREFIX" @save="save(props.item.ID, props.item.PREFIX, 'PREFIX', 'File_Specs')" @cancel="cancel" @open="open" persistent>
                                                {{ props.item.PREFIX }}
                                                <template v-slot:input>
                                                    <v-text-field v-model="props.item.PREFIX" label="Edit" single-line counter></v-text-field>
                                                </template>
                                            </v-edit-dialog>
                                        </template>
                                        <template v-slot:item.DATATYPE="props">
                                            <v-edit-dialog :return-value.sync="props.item.DATATYPE" @save="save(props.item.ID, props.item.DATATYPE, 'DATATYPE', 'File_Specs')" @cancel="cancel" @open="open" persistent>
                                                {{ props.item.DATATYPE }}
                                                <template v-slot:input>
                                                    <v-text-field v-model="props.item.DATATYPE" label="Edit" single-line counter></v-text-field>
                                                </template>
                                            </v-edit-dialog>
                                        </template>
                                        <template v-slot:item.DESC="props">
                                            <v-edit-dialog :return-value.sync="props.item.DESC" @save="save(props.item.ID, props.item.DESC, 'DESC', 'File_Specs')" @cancel="cancel" @open="open" persistent>
                                                {{ props.item.DESC }}
                                                <template v-slot:input>
                                                    <v-text-field v-model="props.item.DESC" label="Edit" single-line counter></v-text-field>
                                                </template>
                                            </v-edit-dialog>
                                        </template>
                                        <template v-slot:item.ISENABLE="props">
                                            <v-edit-dialog :return-value.sync="props.item.ISENABLE" @save="save(props.item.ID, props.item.ISENABLE, 'ISENABLE', 'File_Specs')" @cancel="cancel" @open="open" persistent>
                                                <v-chip :color="getColor(props.item.ISENABLE)" dark>
                                                    {{ props.item.ISENABLE }}
                                                </v-chip>
                                                <template v-slot:input>
                                                    <v-text-field v-model="props.item.ISENABLE" :rules="[isBinary]" label="Edit" single-line counter></v-text-field>
                                                </template>
                                            </v-edit-dialog>
                                        </template>
                                        <template v-slot:item.IsAppend="props">
                                            <v-edit-dialog :return-value.sync="props.item.IsAppend" @save="save(props.item.ID, props.item.IsAppend, 'IsAppend', 'File_Specs')" @cancel="cancel" @open="open" persistent>
                                                <v-chip :color="getColor(props.item.IsAppend)" dark>
                                                    {{ props.item.IsAppend }}
                                                </v-chip>
                                                <template v-slot:input>
                                                    <v-text-field v-model="props.item.IsAppend" :rules="[isBinary]" label="Edit" single-line counter></v-text-field>
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
                                <!-- Rule Dictionary -->
                                <div id="rule_dictionary">
                                    <v-data-table :headers="headers_rule_dictionary" :items="datum_rule_dictionary" :search="search[11]" multi-sort :loading="tableLoad[11]" loading-text="Fetching data... Please wait" class="elevation-5 newline">
                                        <template v-slot:top>
                                            <v-toolbar flat>
                                                <v-toolbar-title class="tableHeader"> Rule Dictionary </v-toolbar-title>
                                                <v-divider class="mx-4" inset vertical></v-divider>
                                                <v-spacer></v-spacer>
                                                <v-text-field v-model="search[11]" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
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
                        </v-row>
                    </v-container>
                </v-main>
            </v-app>
        </div>
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
                // form variables
                valid: true,
                new_valid: true,
                password: '',
                passwordRules: [
                    v => !!v || 'Password is required',
                    v => (v && v.length <= 10) || 'Password must be less than 30 characters',
                ],
                email: '',
                emailRules: [
                    v => !!v || 'E-mail is required',
                    v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
                ],
                value: String,
                // data variables
                num: null,
                backend: "http://10.0.100.146:5555",
                tableLoadCount: 12,
                status_message: null,
                job_name: '',
                job_steps: [],
                start_step: null,
                gif_path: 'blank.png',
                search: [],
                database: null,
                server: null,
                servers: ['US-BCKND', 'QA-US-BCKND'],
                databases: [],
                tableLoad: [false, false, false, false, false, false, false, false, false, false, false, false, false],
                commit: false,
                job_execution: false,
                job_status: null,
                reset_workbench: false,
                reset_defer: false,
                drawer: false,
                snack: false,
                selectSnack: false,
                executionSnack: false,
                snackColor: '',
                snackText: '',
                max25chars: v => v.length <= 25 || 'Input too long!',
                isBinary: v => v >= 0 && v <= 1 || 'Value must be binary',
                maxTimeFrame: v => v >= 1 && v <= 12 || 'Last I checked, there are 12 months in a year!',
                is_authenticated: false,
                pagination: {},
                update_tables: ['kri_details', 'kri_parameters', 'file_specs'],
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
                    { text: 'Lookback Period', value: 'lookback_period' }
                ],
                headers_algo_dictionary: [
                    { text: 'ID', value: 'ID' },
                    { text: 'AlgoName', value: 'AlgoName' },
                    { text: 'AlgoMethod', value: 'AlgoMethod' },
                    { text: 'UpdatedBy', value: 'UpdatedBy' }
                ],
                headers_execution_time: [
                    { text: 'Id', value: 'Id' },
                    { text: 'Stage', value: 'Stage' },
                    { text: 'Procedure', value: 'Procedure' },
                    { text: 'TimeTaken', value: 'TimeTaken' },
                    { text: 'StartTime', value: 'StartTime' },
                    { text: 'EndTime', value: 'EndTime' }
                ],
                headers_file_specs: [
                    { text: 'ID', value: 'ID' },
                    { text: 'FILE_TYPE', value: 'FILE_TYPE' },
                    { text: 'PREFIX', value: 'PREFIX' },
                    { text: 'DATATYPE', value: 'DATATYPE' },
                    { text: 'DESC', value: 'DESC' },
                    { text: 'UPDATED_DATE', value: 'UPDATED_DATE' },
                    { text: 'UPDATED_BY', value: 'UPDATED_BY' },
                    { text: 'ISENABLE', value: 'ISENABLE' },
                    { text: 'IsAppend', value: 'IsAppend' }
                ],
                headers_rule_dictionary: [
                    { text: 'ID', value: 'ID' },
                    { text: 'RuleLevel', value: 'RuleLevel' },
                    { text: 'RuleCategory', value: 'RuleCategory' },
                    { text: 'RuleName', value: 'RuleName' },
                    { text: 'RuleCommand', value: 'RuleCommand' },
                    { text: 'RuleDescription', value: 'RuleDescription' }
                ],
                headers_risk_audit: [
                    { text: 'ID', value: 'ID' },
                    { text: 'DataType', value: 'DataType' },
                    { text: 'ID', value: 'ID' },
                    { text: 'KRIID', value: 'KRIID' },
                    { text: 'Status', value: 'Status' },
                    { text: 'Error Description', value: 'error_description' },
                    { text: 'Start Time', value: 'Start_time' },
                    { text: 'Time Span', value: 'TimeSpan' },
                    { text: 'Updated By', value: 'UpdatedBy' }
                ],
                datum_kri: [],
                datum_params: [],
                datum_algo_params: [],
                datum_errors: [],
                datum_time_frame: [],
                datum_transactions: [],
                datum_warnings: [],
                datum_lookback: [],
                datum_algo_dictionary: [],
                datum_execution_time: [],
                datum_file_specs: [],
                datum_rule_dictionary: [],
                datum_risk_audit: [],
                queries: []
            }
        },
        computed: {
            databaseUpdate() {
                return this.database == null ? true : false;
            }
        },
        watch: {
            database() {
                this.queries = [];
            }
        },
        methods: {
            getDatabases() {
                let auth = {
                    username: this.email,
                    password: this.password
                };
                axios.get(this.backend + '/getDatabaseName?server=' + this.server, {
                    auth: auth
                }).then(response => {
                    this.databases = Object.values(JSON.parse(response.data));
                }).catch(err => {
                    console.log(err);
                });
            },
            jobName() {
                if (this.database == 'ComplianceMonitoring') this.job_name = 'ComplianceMonitoringDemo';
                else if (this.database != null) this.job_name = this.database.replaceAll('_', '');

                let auth = {
                    username: this.email,
                    password: this.password
                };
                axios.get(this.backend + '/jobSteps?server=' + this.server + '&job_name=' + this.job_name, {
                    auth: auth
                }).then(response => {
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
                let auth = {
                    username: this.email,
                    password: this.password
                };
                axios.post(this.backend + '/jobSteps', updates, {
                    auth: auth
                }).then(response => {
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
            resetWorkbench() {
                this.reset_workbench = true;
				this.queries.push('UPDATE speakerAggregateRiskScore SET in_workbench = 0;');
				this.queries.push('UPDATE speakerAggregateRiskScoreTimeSpan SET in_workbench = 0;');
                this.queries.push('TRUNCATE TABLE workbench_log_attachment;');
                this.queries.push('DELETE FROM workbench_log;');
                this.queries.push('DELETE FROM workbench;');
                this.queries.push('DELETE FROM workbench_entity;');
                let updates = {
                    server: this.server,
                    db: this.database,
                    queries: this.queries
                };
                let auth = {
                    username: this.email,
                    password: this.password
                };
                axios.post(this.backend + '/getData', updates, {
                    auth: auth
                }).then(response => {
                    if (response.status == 400) {
                        this.snackText = 'Could not reset workbench';
                        this.snackColor = 'error';
                        this.executionSnack = true;
                    }
                    else {
                        this.snackText = 'Workbench refreshed. Execute Job to see effects.';
                        this.snackColor = 'success';
                        this.executionSnack = true;
                    }
                    console.log(response.data);
                    this.queries = [];
                    this.reset_workbench = false;
                });
            },
            resetDefer() {
                this.reset_defer = true;
                this.queries.push('UPDATE speakerAggregateRiskScore SET is_defer = 0;');
                this.queries.push('UPDATE speakerAggregateRiskScoreTimeSpan SET is_defer = 0;');
                let updates = {
                    server: this.server,
                    db: this.database,
                    queries: this.queries
                };
                let auth = {
                    username: this.email,
                    password: this.password
                };
                axios.post(this.backend + '/getData', updates, {
                    auth: auth
                }).then(response => {
                    if (response.status == 400) {
                        this.snackText = 'Could not reset defer list';
                        this.snackColor = 'error';
                        this.executionSnack = true;
                    }
                    else {
                        this.snackText = 'Defer list refreshed. Execute Job to see effects.';
                        this.snackColor = 'success';
                        this.executionSnack = true;
                    }
                    console.log(response.data);
                    this.queries = [];
                    this.reset_defer = false;
                });
            },
            save(id, newValue, column, table) {
                this.snack = true
                this.snackColor = 'success'
                this.snackText = 'Data saved'
                //if (column == 'is_active' && (newValue != 0 && newValue != 1)) newValue = 0
                if (this.update_tables.indexOf(table) !== -1) {
                    this.queries.push('UPDATE ' + table + ' SET ' + column + ' = ' + newValue + ', updated_date = GETDATE(), updated_by = ' + '\'' + this.email + '\'' + ' WHERE ID = ' + id);
                }
                else this.queries.push('UPDATE ' + table + ' SET ' + column + ' = ' + newValue + ' WHERE ID = ' + id);
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
                let auth = {
                    username: this.email,
                    password: this.password
                };
                axios.post(this.backend + '/getData', updates, {
                    auth: auth
                }).then(response => {
                    if (response.status == 400) {
                        this.snackText = 'Could not commit changes';
                        this.snackColor = 'error';
                        this.executionSnack = true;
                    }
                    else if (response.status == 200) {
                        this.snackText = 'Changes commited';
                        this.snackColor = 'success';
                        this.executionSnack = true;
                    }
                    console.log(response.data);
                    this.queries = [];
                    this.commit = false;
                }).catch(err => {
                    console.log(err);
                    this.snackText = 'Could not commit changes';
                    this.snackColor = 'error';
                    this.executionSnack = true;
                    this.commit = false;
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
            // form validation
            validate(status) {
                let credentials = {
                    email: this.email,
                    password: this.password,
                    new_user: status
                };
                axios.post(this.backend + '/login', credentials).then(response => {
                    this.is_authenticated = response.data;
                    if (this.is_authenticated && response.status == 200) {
                        this.snackText = 'Welcome!';
                        this.snackColor = 'success';
                        this.executionSnack = true;
                    }
                    else if (response.status == 201) {
                        this.snackText = 'Your user has been created. Please login now.';
                        this.snackColor = 'success';
                        this.executionSnack = true;
                    }
                    else {
                        this.snackText = '401 Unauthorized!';
                        this.snackColor = 'error';
                        this.executionSnack = true;
                    }
                }).catch(err => {
                    console.log(err);
                    this.executionSnack = true;
                    this.snackColor = 'error';
                    this.snackText = '401 Unauthorized!';
                });
            },
            // logout
            logout() {
                this.password = '';
                this.is_authenticated = false;
            },
            // fetching data
            async fetchData() {
                this.tableLoadCount = -1;
                if (this.database === null || this.server === null) {
                    this.selectSnack = true
                    this.snackColor = 'error'
                    this.snackText = 'Please make sure server and database is selected'
                }
                else {
                    let auth = {
                        username: this.email,
                        password: this.password
                    };
                    this.tableLoad.fill(true);
                    // Fetch kri_details
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=kri_details&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_kri = Object.values(JSON.parse(response.data));
                        this.tableLoad[0] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch kri_parameters
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=kri_parameters&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_params = Object.values(JSON.parse(response.data));
                        this.tableLoad[1] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch RiskAlgoParameters
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=RiskAlgoParameters&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_algo_params = Object.values(JSON.parse(response.data));
                        this.tableLoad[2] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch ValidationErrors
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=ValidationErrors&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_errors = Object.values(JSON.parse(response.data));
                    }).catch(err => {
                        console.log(err);
                    }).finally(() => {
                        this.tableLoad[3] = false;
                        this.tableLoadCount++;
                        this.verifyStatus();
                    });
                    // Fetch time_frames
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=time_frames&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_time_frame = Object.values(JSON.parse(response.data));
                        this.tableLoad[4] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch RiskyTransactions
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=RiskyTransactions&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_transactions = Object.values(JSON.parse(response.data));
                    }).catch(err => {
                        console.log(err);
                    }).finally(() => {
                        this.tableLoad[5] = false;
                        this.tableLoadCount++;
                        this.verifyStatus();
                    });
                    // Fetch WarningTable
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=WarningTable&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_warnings = Object.values(JSON.parse(response.data));
                    }).catch(err => {
                        console.log(err);
                    }).finally(() => {
                        this.tableLoad[6] = false;
                        this.tableLoadCount++;
                        this.verifyStatus();
                    });
                    // Fetch Lookback Configuration
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=lookback_configuration&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_lookback = Object.values(JSON.parse(response.data));
                    }).catch(err => {
                        console.log(err);
                    }).finally(() => {
                        this.tableLoad[7] = false;
                        this.tableLoadCount++;
                    });
                    // Fetch Risk Algo Dictionary
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=RiskAlgoDictionary&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_algo_dictionary = Object.values(JSON.parse(response.data));
                        this.tableLoad[8] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch Execution Time Log
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=ExecutionTimeLog&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_execution_time = Object.values(JSON.parse(response.data));
                    }).catch(err => {
                        console.log(err);
                    }).finally(() => {
                        this.tableLoad[9] = false;
                        this.tableLoadCount++;
                    });
                    // Fetch File Specs
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=File_Specs&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_file_specs = Object.values(JSON.parse(response.data));
                        this.tableLoad[10] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch Rule Dictionary
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=RuleDictionary&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_rule_dictionary = Object.values(JSON.parse(response.data));
                        this.tableLoad[11] = false;
                        this.tableLoadCount++;
                    }).catch(err => {
                        console.log(err);
                    });
                    // Fetch Risk Audit Logs
                    axios.get(this.backend + '/getData?db=' + this.database + '&table=RiskAuditLogs&server=' + this.server, {
                        auth: auth
                    }).then(response => {
                        this.datum_risk_audit = Object.values(JSON.parse(response.data));
                        this.tableLoad[12] = false;
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