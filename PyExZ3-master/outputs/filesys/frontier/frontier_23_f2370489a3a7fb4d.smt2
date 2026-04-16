(set-logic ALL)
; Constraint ID: f2370489a3a7fb4d
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60019)) (False)
(assert (not (= x 60019)))

; Query: ((== x 60020)) (False)
(assert (not (not (= x 60020))))

(check-sat)
(get-model)
