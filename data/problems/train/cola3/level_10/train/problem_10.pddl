

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b1)
(on b3 b5)
(on b4 b2)
(ontable b5)
(on b6 b9)
(ontable b7)
(on b8 b12)
(on b9 b11)
(on b10 b8)
(ontable b11)
(on b12 b6)
(clear b4)
(clear b7)
(clear b10)
)
(:goal
(and
(on b3 b12)
(on b4 b8)
(on b6 b7)
(on b7 b1)
(on b10 b3)
(on b11 b6))
)
)


