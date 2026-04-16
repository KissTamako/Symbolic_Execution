(set-logic ALL)
; Path ID: a594acfa55811ffd
; Generated at: 2026-04-16 12:01:19
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const x Int)
(declare-const y Int)

; (x) (False)
(assert (not x))

; Query: (y) (True)
(assert (not y))

(check-sat)
(get-model)
