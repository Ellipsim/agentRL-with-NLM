

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b10)
(ontable b2)
(on b3 b8)
(ontable b4)
(on b5 b3)
(on b6 b4)
(on b7 b6)
(on b8 b2)
(ontable b9)
(on b10 b7)
(clear b1)
(clear b5)
(clear b9)
)
(:goal
(and
(on b1 b3)
(on b2 b9)
(on b3 b8)
(on b4 b10)
(on b5 b7)
(on b6 b5)
(on b7 b4)
(on b9 b6))
)
)


