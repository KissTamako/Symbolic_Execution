(set-logic ALL)
; Constraint ID: 19800bc784eafb96
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59551)) (False)
(assert (not (= x 59551)))

; Query: ((== x 59552)) (False)
(assert (not (not (= x 59552))))

(check-sat)
(get-model)
