

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b9)
(on b3 b5)
(on b4 b8)
(on-table b5)
(on b6 b4)
(on-table b7)
(on-table b8)
(on-table b9)
(clear b1)
(clear b3)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b7)
(on b3 b2)
(on b4 b8)
(on b6 b9)
(on b7 b6)
(on b8 b1)
(on b9 b3))
)
)


