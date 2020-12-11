--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5
-- Dumped by pg_dump version 12.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: gender; Type: TYPE; Schema: public; Owner: none
--

CREATE TYPE public.gender AS ENUM (
    'male',
    'female',
    'other'
);


ALTER TYPE public.gender OWNER TO none;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actor_movie; Type: TABLE; Schema: public; Owner: None
--

CREATE TABLE public.actor_movie (
    actor_id integer NOT NULL,
    movie_id integer NOT NULL
);


ALTER TABLE public.actor_movie OWNER TO none;

--
-- Name: actors; Type: TABLE; Schema: public; Owner: none
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying NOT NULL,
    "DOB" date NOT NULL,
    gender public.gender NOT NULL
);


ALTER TABLE public.actors OWNER TO none;

--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: none
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO none;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: none
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- Name: movies; Type: TABLE; Schema: public; Owner: none
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying NOT NULL,
    release_date date NOT NULL
);


ALTER TABLE public.movies OWNER TO none;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: none
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO none;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: none
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: none
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: none
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Data for Name: actor_movie; Type: TABLE DATA; Schema: public; Owner: none
--

COPY public.actor_movie (actor_id, movie_id) FROM stdin;
2	2
3	3
1	1
\.


--
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: none
--

COPY public.actors (id, name, "DOB", gender) FROM stdin;
1	jake	2020-12-10	male
2	vic	2020-12-10	female
3	ella	2020-12-10	other
4	pedro	2020-12-10	male
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: none
--

COPY public.movies (id, title, release_date) FROM stdin;
1	The Movie	2020-12-10
2	The Not Movie	2020-12-10
3	The Third Movie	2020-12-10
\.


--
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: none
--

SELECT pg_catalog.setval('public.actors_id_seq', 4, true);


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: none
--

SELECT pg_catalog.setval('public.movies_id_seq', 3, true);


--
-- Name: actor_movie actor_movie_pkey; Type: CONSTRAINT; Schema: public; Owner: none
--

ALTER TABLE ONLY public.actor_movie
    ADD CONSTRAINT actor_movie_pkey PRIMARY KEY (actor_id, movie_id);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: none
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: none
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- Name: actor_movie actor_movie_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: none
--

ALTER TABLE ONLY public.actor_movie
    ADD CONSTRAINT actor_movie_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actors(id);


--
-- Name: actor_movie actor_movie_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: none
--

ALTER TABLE ONLY public.actor_movie
    ADD CONSTRAINT actor_movie_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id);


--
-- PostgreSQL database dump complete
--

