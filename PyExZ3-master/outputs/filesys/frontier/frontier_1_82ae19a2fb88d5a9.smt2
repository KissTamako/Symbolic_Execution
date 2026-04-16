(set-logic ALL)
; Constraint ID: 82ae19a2fb88d5a9
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59911)) (False)
(assert (not (= x 59911)))

; Query: ((== x 59912)) (False)
(assert (not (not (= x 59912))))

(check-sat)
(get-model)
