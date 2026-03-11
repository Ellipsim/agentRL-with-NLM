

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b8)
(on b3 b4)
(on b4 b9)
(on-table b5)
(on-table b6)
(on b7 b5)
(on-table b8)
(on b9 b10)
(on-table b10)
(clear b1)
(clear b2)
(clear b3)
(clear b7)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
(on b4 b9)
(on b5 b7)
(on b7 b6)
(on b8 b4)
(on b9 b5)
(on b10 b1))
)
)


