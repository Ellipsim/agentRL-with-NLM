

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b7)
(ontable b2)
(on b3 b11)
(ontable b4)
(on b5 b4)
(ontable b6)
(on b7 b5)
(on b8 b6)
(on b9 b12)
(on b10 b1)
(on b11 b8)
(on b12 b10)
(clear b2)
(clear b3)
(clear b9)
)
(:goal
(and
(on b1 b8)
(on b2 b11)
(on b5 b4)
(on b6 b7)
(on b8 b5)
(on b9 b10)
(on b10 b2)
(on b12 b1))
)
)


