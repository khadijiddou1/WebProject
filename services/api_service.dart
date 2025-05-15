// lib/services/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000/api'; // Replace with your actual backend URL
  String? authToken;

  // Initialize with saved token if available
  ApiService() {
    _loadToken();
  }

  Future<void> _saveToken(String token) async {
  authToken = token;
  final prefs = await SharedPreferences.getInstance();
  await prefs.setString('authToken', token);
}

Future<void> _loadToken() async {
  final prefs = await SharedPreferences.getInstance();
  authToken = prefs.getString('authToken');
}

Future<void> _clearToken() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.remove('authToken');
  authToken = null;
}

  // Authentication
  Future<Map<String, dynamic>> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/token/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'username': username,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      await _saveToken(data['access']);
      return data;
    } else {
      throw Exception('Failed to login: ${response.statusCode}');
    }
  }

  Future<Map<String, dynamic>> refreshToken(String refreshToken) async {
    final response = await http.post(
      Uri.parse('$baseUrl/token/refresh/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'refresh': refreshToken}),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      await _saveToken(data['access']);
      return data;
    } else {
      await _clearToken();
      throw Exception('Failed to refresh token');
    }
  }

  // Registration
  Future<Map<String, dynamic>> registerClient(Map<String, dynamic> userData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/register/client/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(userData),
    );

    if (response.statusCode == 201) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to register client: ${response.statusCode}');
    }
  }

  Future<Map<String, dynamic>> registerFournisseur(Map<String, dynamic> userData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/register/fournisseur/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(userData),
    );

    if (response.statusCode == 201) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to register fournisseur: ${response.statusCode}');
    }
  }

  // User Profile
  Future<Map<String, dynamic>> getUserProfile() async {
    final response = await http.get(
      Uri.parse('$baseUrl/user/profile/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $authToken',
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else if (response.statusCode == 401) {
      await _clearToken();
      throw Exception('Session expired');
    } else {
      throw Exception('Failed to get user profile: ${response.statusCode}');
    }
  }

 Future<List<dynamic>> getProducts() async {
    final response = await http.get(
      Uri.parse('$baseUrl/products/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $authToken',
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load products');
    }
  }

  Future<List<dynamic>> getOrders() async {
    final response = await http.get(
      Uri.parse('$baseUrl/orders/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $authToken',
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load orders');
    }
  }
  // Add other API methods as needed...
}