

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b2)
(on-table b2)
(on b3 b4)
(on b4 b5)
(on-table b5)
(on b6 b1)
(on b7 b3)
(on b8 b7)
(on-table b9)
(clear b6)
(clear b8)
(clear b9)
)
(:goal
(and
(on b2 b5)
(on b3 b2)
(on b4 b1)
(on b5 b7)
(on b6 b3)
(on b8 b9)
(on b9 b4))
)
)


