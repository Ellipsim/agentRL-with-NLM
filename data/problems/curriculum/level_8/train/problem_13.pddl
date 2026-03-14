

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b7)
(on-table b2)
(on b3 b6)
(on b4 b9)
(on b5 b4)
(on b6 b1)
(on-table b7)
(on-table b8)
(on b9 b2)
(clear b3)
(clear b5)
(clear b8)
)
(:goal
(and
(on b2 b5)
(on b3 b2)
(on b4 b6)
(on b9 b3))
)
)


