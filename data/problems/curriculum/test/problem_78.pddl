

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b8)
(on b3 b1)
(on-table b4)
(on b5 b7)
(on b6 b9)
(on-table b7)
(on b8 b6)
(on b9 b5)
(clear b2)
(clear b3)
)
(:goal
(and
(on b2 b9)
(on b4 b1)
(on b5 b7)
(on b7 b2)
(on b9 b8))
)
)


