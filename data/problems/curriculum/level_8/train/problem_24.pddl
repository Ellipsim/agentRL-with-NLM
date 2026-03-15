

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 )
(:init
(arm-empty)
(on b1 b8)
(on-table b2)
(on b3 b9)
(on-table b4)
(on b5 b3)
(on b6 b2)
(on-table b7)
(on b8 b5)
(on-table b9)
(clear b1)
(clear b4)
(clear b6)
(clear b7)
)
(:goal
(and
(on b2 b5)
(on b4 b7)
(on b5 b4)
(on b6 b2)
(on b7 b9)
(on b9 b1))
)
)


