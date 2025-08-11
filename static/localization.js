/**
 * Localization Support for n8n AI Agent Web Interface
 * Šis fails nodrošina daudzvalodu atbalstu web saskarnei.
 */

class LocalizationManager {
    constructor() {
        this.currentLanguage = 'lv'; // Noklusējuma valoda
        this.translations = {
            'lv': {
                // Galvenie elementi
                'title': 'n8n AI Aģents',
                'subtitle': 'Pārveidojiet dabisku valodu par n8n workflow',
                'query_label': 'Jūsu pieprasījums (latviešu, krievu vai angļu valodā):',
                'query_placeholder': 'Piemēram: Izveidot Telegram botu pierakstam uz tikšanos ar datu bāzes integrāciju...',
                'max_results_label': 'Maksimālais līdzīgo workflow skaits:',
                
                // Pogas
                'btn_generate': '🚀 Ģenerēt Workflow',
                'btn_search': '🔍 Meklēt Līdzīgus',
                'btn_health': '❤️ Pārbaudīt Sistēmu',
                'btn_stats': '📊 Statistika',
                'btn_n8n_config': '⚙️ n8n Konfigurācija',
                'btn_upload_n8n': '📤 Augšupielādēt uz n8n',
                
                // Rezultātu sadaļas
                'results_title': 'Rezultāti',
                'workflow_generation_title': '🎯 Workflow Ģenerēšanas Rezultāts',
                'query_analysis_title': '📝 Vaicājuma Analīze',
                'workflow_json_title': '🔧 Workflow JSON',
                'setup_instructions_title': '📋 Uzstādīšanas Instrukcijas',
                'explanation_title': '💡 Paskaidrojums',
                'errors_title': '⚠️ Kļūdas',
                'search_results_title': '🔍 Meklēšanas Rezultāti',
                'system_health_title': '❤️ Sistēmas Stāvoklis',
                'statistics_title': '📊 Sistēmas Statistika',
                
                // Statistikas lauki
                'stat_language': 'Valoda',
                'stat_keywords': 'Atslēgvārdi',
                'stat_similar_workflows': 'Līdzīgi workflow',
                'stat_available_nodes': 'Pieejamie mezgli',
                'stat_nodes_available': 'Pieejamie mezgli',
                'stat_workflows_in_db': 'Workflow bāzē',
                
                // Ziņojumi
                'loading_generate': 'Ģenerē workflow...',
                'loading_search': 'Meklē līdzīgus workflow...',
                'loading_health': 'Pārbauda sistēmas stāvokli...',
                'loading_stats': 'Iegūst statistiku...',
                'loading_upload': 'Augšupielādē uz n8n...',
                
                // Kļūdu ziņojumi
                'error_empty_query': 'Lūdzu, ievadiet pieprasījumu!',
                'error_connection': 'Savienojuma kļūda',
                'error_generation': 'Workflow ģenerēšanas kļūda',
                'error_search': 'Meklēšanas kļūda',
                'error_health': 'Nevar pārbaudīt sistēmas stāvokli',
                'error_stats': 'Nevar iegūt statistiku',
                'error_n8n_config': 'n8n konfigurācijas kļūda',
                
                // Veiksmes ziņojumi
                'success_generated': 'Workflow veiksmīgi ģenerēts',
                'success_uploaded': 'Workflow veiksmīgi augšupielādēts uz n8n',
                'success_health': 'Sistēma darbojas normāli',
                'success_n8n_config': 'n8n savienojums konfigurēts',
                
                // n8n integrācija
                'n8n_config_title': '⚙️ n8n Konfigurācija',
                'n8n_url_label': 'n8n Servera URL:',
                'n8n_api_key_label': 'API Atslēga:',
                'n8n_test_connection': 'Testēt Savienojumu',
                'n8n_save_config': 'Saglabāt Konfigurāciju',
                'n8n_upload_options': 'Augšupielādes Opcijas',
                'n8n_activate_workflow': 'Aktivizēt workflow pēc augšupielādes',
                'n8n_test_execution': 'Testēt workflow izpildi',
                
                // Valodu izvēle
                'language_selector': 'Valoda:',
                'language_lv': 'Latviešu',
                'language_ru': 'Русский',
                'language_en': 'English',
                
                // Papildu
                'no_results': 'Nav rezultātu',
                'similarity_score': 'Līdzības punkti',
                'match_reasons': 'Atbilstības iemesli',
                'suggested_modifications': 'Ieteiktās modificēšanas',
                'view_workflow_json': 'Skatīt workflow JSON',
                'component_status': 'Komponentu stāvoklis',
                'active': 'Aktīvs',
                'inactive': 'Neaktīvs',
                'connected': 'Savienots',
                'disconnected': 'Atvienots'
            },
            
            'ru': {
                // Галвные элементы
                'title': 'n8n AI Агент',
                'subtitle': 'Превратите естественный язык в n8n workflow',
                'query_label': 'Ваш запрос (на латышском, русском или английском языке):',
                'query_placeholder': 'Например: Создать Telegram бота для записи на встречи с интеграцией базы данных...',
                'max_results_label': 'Максимальное количество похожих workflow:',
                
                // Кнопки
                'btn_generate': '🚀 Генерировать Workflow',
                'btn_search': '🔍 Искать Похожие',
                'btn_health': '❤️ Проверить Систему',
                'btn_stats': '📊 Статистика',
                'btn_n8n_config': '⚙️ Конфигурация n8n',
                'btn_upload_n8n': '📤 Загрузить в n8n',
                
                // Разделы результатов
                'results_title': 'Результаты',
                'workflow_generation_title': '🎯 Результат Генерации Workflow',
                'query_analysis_title': '📝 Анализ Запроса',
                'workflow_json_title': '🔧 Workflow JSON',
                'setup_instructions_title': '📋 Инструкции по Установке',
                'explanation_title': '💡 Объяснение',
                'errors_title': '⚠️ Ошибки',
                'search_results_title': '🔍 Результаты Поиска',
                'system_health_title': '❤️ Состояние Системы',
                'statistics_title': '📊 Статистика Системы',
                
                // Поля статистики
                'stat_language': 'Язык',
                'stat_keywords': 'Ключевые слова',
                'stat_similar_workflows': 'Похожие workflow',
                'stat_available_nodes': 'Доступные узлы',
                'stat_nodes_available': 'Доступные узлы',
                'stat_workflows_in_db': 'Workflow в базе',
                
                // Сообщения
                'loading_generate': 'Генерирую workflow...',
                'loading_search': 'Ищу похожие workflow...',
                'loading_health': 'Проверяю состояние системы...',
                'loading_stats': 'Получаю статистику...',
                'loading_upload': 'Загружаю в n8n...',
                
                // Сообщения об ошибках
                'error_empty_query': 'Пожалуйста, введите запрос!',
                'error_connection': 'Ошибка соединения',
                'error_generation': 'Ошибка генерации workflow',
                'error_search': 'Ошибка поиска',
                'error_health': 'Не удается проверить состояние системы',
                'error_stats': 'Не удается получить статистику',
                'error_n8n_config': 'Ошибка конфигурации n8n',
                
                // Сообщения об успехе
                'success_generated': 'Workflow успешно сгенерирован',
                'success_uploaded': 'Workflow успешно загружен в n8n',
                'success_health': 'Система работает нормально',
                'success_n8n_config': 'Соединение с n8n настроено',
                
                // Интеграция n8n
                'n8n_config_title': '⚙️ Конфигурация n8n',
                'n8n_url_label': 'URL сервера n8n:',
                'n8n_api_key_label': 'API ключ:',
                'n8n_test_connection': 'Тестировать Соединение',
                'n8n_save_config': 'Сохранить Конфигурацию',
                'n8n_upload_options': 'Опции Загрузки',
                'n8n_activate_workflow': 'Активировать workflow после загрузки',
                'n8n_test_execution': 'Тестировать выполнение workflow',
                
                // Выбор языка
                'language_selector': 'Язык:',
                'language_lv': 'Latviešu',
                'language_ru': 'Русский',
                'language_en': 'English',
                
                // Дополнительно
                'no_results': 'Нет результатов',
                'similarity_score': 'Баллы сходства',
                'match_reasons': 'Причины соответствия',
                'suggested_modifications': 'Предлагаемые изменения',
                'view_workflow_json': 'Посмотреть workflow JSON',
                'component_status': 'Состояние компонентов',
                'active': 'Активен',
                'inactive': 'Неактивен',
                'connected': 'Подключен',
                'disconnected': 'Отключен'
            },
            
            'en': {
                // Main elements
                'title': 'n8n AI Agent',
                'subtitle': 'Transform natural language into n8n workflows',
                'query_label': 'Your request (in Latvian, Russian, or English):',
                'query_placeholder': 'For example: Create a Telegram bot for appointment booking with database integration...',
                'max_results_label': 'Maximum number of similar workflows:',
                
                // Buttons
                'btn_generate': '🚀 Generate Workflow',
                'btn_search': '🔍 Search Similar',
                'btn_health': '❤️ Check System',
                'btn_stats': '📊 Statistics',
                'btn_n8n_config': '⚙️ n8n Configuration',
                'btn_upload_n8n': '📤 Upload to n8n',
                
                // Result sections
                'results_title': 'Results',
                'workflow_generation_title': '🎯 Workflow Generation Result',
                'query_analysis_title': '📝 Query Analysis',
                'workflow_json_title': '🔧 Workflow JSON',
                'setup_instructions_title': '📋 Setup Instructions',
                'explanation_title': '💡 Explanation',
                'errors_title': '⚠️ Errors',
                'search_results_title': '🔍 Search Results',
                'system_health_title': '❤️ System Health',
                'statistics_title': '📊 System Statistics',
                
                // Statistics fields
                'stat_language': 'Language',
                'stat_keywords': 'Keywords',
                'stat_similar_workflows': 'Similar workflows',
                'stat_available_nodes': 'Available nodes',
                'stat_nodes_available': 'Available nodes',
                'stat_workflows_in_db': 'Workflows in database',
                
                // Messages
                'loading_generate': 'Generating workflow...',
                'loading_search': 'Searching similar workflows...',
                'loading_health': 'Checking system health...',
                'loading_stats': 'Getting statistics...',
                'loading_upload': 'Uploading to n8n...',
                
                // Error messages
                'error_empty_query': 'Please enter a request!',
                'error_connection': 'Connection error',
                'error_generation': 'Workflow generation error',
                'error_search': 'Search error',
                'error_health': 'Cannot check system health',
                'error_stats': 'Cannot get statistics',
                'error_n8n_config': 'n8n configuration error',
                
                // Success messages
                'success_generated': 'Workflow generated successfully',
                'success_uploaded': 'Workflow uploaded to n8n successfully',
                'success_health': 'System is running normally',
                'success_n8n_config': 'n8n connection configured',
                
                // n8n integration
                'n8n_config_title': '⚙️ n8n Configuration',
                'n8n_url_label': 'n8n Server URL:',
                'n8n_api_key_label': 'API Key:',
                'n8n_test_connection': 'Test Connection',
                'n8n_save_config': 'Save Configuration',
                'n8n_upload_options': 'Upload Options',
                'n8n_activate_workflow': 'Activate workflow after upload',
                'n8n_test_execution': 'Test workflow execution',
                
                // Language selection
                'language_selector': 'Language:',
                'language_lv': 'Latviešu',
                'language_ru': 'Русский',
                'language_en': 'English',
                
                // Additional
                'no_results': 'No results',
                'similarity_score': 'Similarity score',
                'match_reasons': 'Match reasons',
                'suggested_modifications': 'Suggested modifications',
                'view_workflow_json': 'View workflow JSON',
                'component_status': 'Component status',
                'active': 'Active',
                'inactive': 'Inactive',
                'connected': 'Connected',
                'disconnected': 'Disconnected'
            }
        };
        
        // Automātiski nosaka valodu no pārlūkprogrammas
        this.detectBrowserLanguage();
    }
    
    detectBrowserLanguage() {
        const browserLang = navigator.language || navigator.userLanguage;
        
        if (browserLang.startsWith('lv')) {
            this.currentLanguage = 'lv';
        } else if (browserLang.startsWith('ru')) {
            this.currentLanguage = 'ru';
        } else {
            this.currentLanguage = 'en';
        }
        
        // Pārbauda localStorage
        const savedLang = localStorage.getItem('n8n_ai_agent_language');
        if (savedLang && this.translations[savedLang]) {
            this.currentLanguage = savedLang;
        }
    }
    
    setLanguage(language) {
        if (this.translations[language]) {
            this.currentLanguage = language;
            localStorage.setItem('n8n_ai_agent_language', language);
            this.updateUI();
        }
    }
    
    getCurrentLanguage() {
        return this.currentLanguage;
    }
    
    t(key, defaultValue = null) {
        const translation = this.translations[this.currentLanguage];
        return translation[key] || defaultValue || key;
    }
    
    updateUI() {
        // Atjaunina visus elementus ar data-i18n atribūtu
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' && element.type !== 'button') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });
        
        // Atjaunina title un meta tagus
        document.title = this.t('title') + ' - ' + this.t('subtitle');
        
        // Atjaunina valodu izvēles pogu
        this.updateLanguageSelector();
    }
    
    updateLanguageSelector() {
        const selector = document.getElementById('languageSelector');
        if (selector) {
            // Atjaunina izvēlēto opciju
            selector.value = this.currentLanguage;
        }
    }
    
    createLanguageSelector() {
        const selector = document.createElement('select');
        selector.id = 'languageSelector';
        selector.className = 'language-selector';
        
        const languages = [
            { code: 'lv', name: this.t('language_lv') },
            { code: 'ru', name: this.t('language_ru') },
            { code: 'en', name: this.t('language_en') }
        ];
        
        languages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.code;
            option.textContent = lang.name;
            if (lang.code === this.currentLanguage) {
                option.selected = true;
            }
            selector.appendChild(option);
        });
        
        selector.addEventListener('change', (e) => {
            this.setLanguage(e.target.value);
        });
        
        return selector;
    }
    
    // Palīgfunkcijas lokalizētiem ziņojumiem
    getLoadingMessage(type) {
        const key = `loading_${type}`;
        return this.t(key, 'Loading...');
    }
    
    getErrorMessage(type) {
        const key = `error_${type}`;
        return this.t(key, 'Error occurred');
    }
    
    getSuccessMessage(type) {
        const key = `success_${type}`;
        return this.t(key, 'Success');
    }
    
    // Formatē skaitļus atbilstoši valodai
    formatNumber(number) {
        return new Intl.NumberFormat(this.getLocale()).format(number);
    }
    
    // Formatē datumu atbilstoši valodai
    formatDate(date) {
        return new Intl.DateTimeFormat(this.getLocale()).format(date);
    }
    
    getLocale() {
        const localeMap = {
            'lv': 'lv-LV',
            'ru': 'ru-RU',
            'en': 'en-US'
        };
        return localeMap[this.currentLanguage] || 'en-US';
    }
}

// Globālais lokalizācijas pārvaldnieks
const i18n = new LocalizationManager();

// Palīgfunkcijas
function t(key, defaultValue = null) {
    return i18n.t(key, defaultValue);
}

function setLanguage(language) {
    i18n.setLanguage(language);
}

function getCurrentLanguage() {
    return i18n.getCurrentLanguage();
}

// Inicializē lokalizāciju, kad lapa ir ielādēta
document.addEventListener('DOMContentLoaded', function() {
    // Pievieno valodu izvēles elementu
    const header = document.querySelector('.header');
    if (header) {
        const languageContainer = document.createElement('div');
        languageContainer.className = 'language-container';
        languageContainer.style.cssText = `
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: white;
        `;
        
        const label = document.createElement('label');
        label.textContent = t('language_selector');
        label.style.fontSize = '14px';
        
        const selector = i18n.createLanguageSelector();
        selector.style.cssText = `
            padding: 5px 10px;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 5px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 14px;
        `;
        
        languageContainer.appendChild(label);
        languageContainer.appendChild(selector);
        header.appendChild(languageContainer);
    }
    
    // Atjaunina UI ar sākotnējo valodu
    i18n.updateUI();
});

// CSS stili lokalizācijai
const localizationStyles = `
    .language-selector {
        transition: all 0.3s ease;
    }
    
    .language-selector:hover {
        background: rgba(255,255,255,0.2) !important;
    }
    
    .language-selector option {
        background: #333;
        color: white;
    }
    
    .language-container {
        z-index: 1000;
    }
`;

// Pievieno stilus
const styleSheet = document.createElement('style');
styleSheet.textContent = localizationStyles;
document.head.appendChild(styleSheet);

// Eksportē globāli
window.i18n = i18n;
window.t = t;
window.setLanguage = setLanguage;
window.getCurrentLanguage = getCurrentLanguage;

