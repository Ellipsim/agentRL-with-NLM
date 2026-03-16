

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b8)
(on b3 b4)
(ontable b4)
(on b5 b6)
(on b6 b12)
(ontable b7)
(ontable b8)
(on b9 b2)
(on b10 b3)
(on b11 b1)
(ontable b12)
(clear b5)
(clear b7)
(clear b10)
(clear b11)
)
(:goal
(and
(on b3 b7)
(on b4 b3)
(on b5 b11)
(on b6 b5)
(on b7 b10)
(on b8 b9)
(on b9 b2)
(on b10 b12)
(on b11 b8))
)
)


