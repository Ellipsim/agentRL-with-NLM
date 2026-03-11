

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b2)
(on-table b4)
(on b5 b8)
(on-table b6)
(on b7 b3)
(on b8 b7)
(on-table b9)
(on b10 b9)
(clear b1)
(clear b4)
(clear b5)
(clear b6)
(clear b10)
)
(:goal
(and
(on b3 b10)
(on b6 b3)
(on b7 b4)
(on b8 b6)
(on b9 b1))
)
)


