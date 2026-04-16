(set-logic ALL)
; Path ID: b6fb39aef9bae917
; Generated at: 2026-04-16 12:01:23
; Solver: Z3Wrapper
; Number of assertions: 2
; Has query: True

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)

; (y) (True)
(assert y)
; (x) (True)
(assert x)

; Query: (z) (True)
(assert (not z))

(check-sat)
(get-model)
