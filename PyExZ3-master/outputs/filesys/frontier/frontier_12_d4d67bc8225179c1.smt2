(set-logic ALL)
; Constraint ID: d4d67bc8225179c1
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60679)) (False)
(assert (not (not (= x 60679))))

(check-sat)
(get-model)
